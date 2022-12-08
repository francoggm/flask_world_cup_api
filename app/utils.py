import random

from .models import Player

def player_have_team(player, user_teams):
    for team in user_teams:
        if player in team.players_owned:
            return True
    return False

def open_package(cards_count = 2):
    players = Player.query.all()
    new_cards = [random.choice(players) for _ in range(cards_count)]
    return new_cards