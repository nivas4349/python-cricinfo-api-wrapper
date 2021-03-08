from flask import Flask, jsonify
from flask_restful import Api
from espncricinfo.player import Player as CricInfoPlayer
from espncricinfo.exceptions import *

PLAYER_HOME_PATH = "/player"
PLAYER_HOME_PATH_WITH_SLASH = "/player/"
BATTING_PATH = "/battingstats"
BOWLING_PATH = "/bowlingstats"
PLAYER_ID_PATH = PLAYER_HOME_PATH + "/<playerId>"

SUMMARY = "summary"
BATTING_STATS = "batting_stats"
BOWLING_STATS = "bowling_stats"

PLAYER_HOME_MSG = "I need Player Id to return stats!"
HOME_MSG = "Welcome to Cricket Player's Stats!!<3"

ERR_DONT_ACT_SMART_VALID_ID = "Enough acting smart, now send me valid Player Id!"
ERR_PLAYER_NOT_FOUND = "Player not found! Check the player Id and try again!"

app = Flask(__name__)
api = Api(app)


class Player:
    @app.route("/")
    def index():
        return HOME_MSG

    @app.route(PLAYER_HOME_PATH)
    def get_player():
        return PLAYER_HOME_MSG

    @app.route(PLAYER_HOME_PATH_WITH_SLASH)
    def get_player_with_slash():
        return PLAYER_HOME_MSG

    @app.route(PLAYER_ID_PATH)
    def get_summary(playerId):
        return f_get_data(playerId, SUMMARY)

    @app.route(PLAYER_ID_PATH + BATTING_PATH)
    def get_battingstats(playerId):
        return f_get_data(playerId, BATTING_STATS)

    @app.route(PLAYER_ID_PATH + BOWLING_PATH)
    def get_bowlingstats(playerId):
        return f_get_data(playerId, BOWLING_STATS)


def f_get_data(playerId, action):
    try:
        p = CricInfoPlayer(int(playerId))
        switcher = {
            SUMMARY: f_get_summary(p),
            BATTING_STATS: jsonify(CricInfoPlayer(int(playerId)).batting_fielding_averages),
            BOWLING_STATS: jsonify(CricInfoPlayer(int(playerId)).bowling_averages)
        }
        return switcher.get(action)
    except ValueError:
        return ERR_DONT_ACT_SMART_VALID_ID, 400
    except PlayerNotFoundError:
        return ERR_PLAYER_NOT_FOUND, 404


def f_get_summary(p):
    data = {'name': p.name, 'firstName': p.first_name, 'fullName': p.full_name, 'dob': p.date_of_birth,
            'age': p.current_age, 'majorTeams': p.major_teams, 'nickName': p.nickname,
            'playingRole': p.playing_role, 'battingStyle': p.batting_style, 'bowlingStyle': p.bowling_style,
            'testDebut': p.test_debut, 'lastTest': p.last_test, 't20iDebut': p.t20i_debut,
            'lastT20i': p.last_t20i,
            'firstClassDebut': p.first_class_debut, 'lastFirstClass': p.last_first_class,
            'listADebut': p.list_a_debut, 'lastListA': p.last_list_a, 't20Debut': p.t20_debut,
            'lastT20': p.last_t20, 'odiDebut': p.odi_debut, 'lastOdi': p.last_odi,
            'recentMatches': p.recent_matches}
    return jsonify(data)


if __name__ == '__main__':
    app.run()
