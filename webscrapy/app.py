from bs4 import BeautifulSoup
from time import sleep
from unidecode import unidecode
from datetime import datetime
from threading import Thread


import requests
import psycopg2
import os
import pandas as pd

base_url = 'https://www.scheduleworld.co/player'

DB_HOST = os.environ.get('DATABASE_HOST')
DB = os.environ.get('DATABASE')
DB_USER = os.environ.get('DATABASE_USER')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')

con = psycopg2.connect(host = DB_HOST, database = DB, user = DB_USER, password = DB_PASSWORD)

def get_players_names():
    res = requests.get(base_url)
    names = []

    if res.text:
            soup = BeautifulSoup(res.text, 'html.parser')

            pages = soup.find('div', class_='pagination').findChild(class_='pages').text
            pages = int(pages.replace('Page 1 of ', ''))

            for i in range(pages):
                print(f'Page {i} of {pages}')
                try:
                    page = requests.get(f'{base_url}/page/{i}')
                    soup = BeautifulSoup(page.text, 'html.parser')
                    players = soup.find('div', class_='post-listing').find_all('article')

                    for article in players:
                        name = article.findChild('a').text.replace(' ', '-').replace('.','').lower()
                        names.append(name)

                except Exception as e:
                    print(e)
            sleep(0.05)
    return names

def get_players_infos(names: list):
    if names:
        queries = []
        count = 0
     
        for player in names:
            try:
                print(f'Player - {player}')

                res = requests.get(f'{base_url}/{unidecode(player)}')
                soup = BeautifulSoup(res.text, 'html.parser')

                players_options = soup.find('div', class_='player-header__options')
                players_stats = soup.find('div', class_='player-stats-pro__wrapper anwp-grid-table')

                if players_options.text.strip() and players_stats.text.strip():
    
                    stats_div = players_stats.findChildren(class_='player-stats-pro__value anwp-text-4xl mt-2')

                    name = players_options.findChild(class_='player-header__option__full_name player-header__option-value').text.strip()
                    position = players_options.findChild(class_='player-header__option__position player-header__option-value').text.strip()
                    birthdate = players_options.findChild(class_='player-header__option__birth_date player-header__option-value').text.strip()
                    weight = players_options.findChild(class_='player-header__option__weight player-header__option-value').text.strip()
                    height = players_options.findChild(class_='player-header__option__height player-header__option-value').text.strip()

                    games_played = stats_div[0].text.strip()
                    minutes_played = stats_div[2].text.strip()
                    cards_yellow = stats_div[3].text.strip()
                    cards_red = stats_div[5].text.strip()
                    goals = stats_div[6].text.strip()

                    birthdate = datetime.strptime(birthdate, '%B %d, %Y').strftime('%Y-%m-%d')

                    queries.append((name, position, birthdate, weight, height, games_played, minutes_played, cards_yellow, cards_red, goals))

                    count += 1

                    if count > 10:
                        save_db = Thread(target = insert_into_db, args=(queries,))
                        save_db.start()

                        count = 0
                        queries = []
                        print('=== Saving players ===')

                sleep(0.05)
            except Exception as e:
                print(e)
        return queries

def insert_into_db(queries):
    cur = con.cursor()

    cur.executemany("INSERT INTO player (name, position, birthdate, weight, height, games_played, minutes_played, cards_yellow, cards_red, goals) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", queries)
    con.commit()

if __name__ == '__main__':
    names = get_players_names()
    queries = get_players_infos(names)

    
    # df = pd.DataFrame(queries, columns=['name', 'position', 'birthdate', 'weight', 'height', 'games_played', 'minutes_played', 'cards_yellow', 'cards_red', 'goals'])
    # df.to_csv('players.csv', index=False)
    # df = pd.read_csv('csv/players.csv')
    # queries = list(df.itertuples(index=False, name=None))
    # names = pd.read_csv('csv/players_names.csv')['0'].to_list()


    