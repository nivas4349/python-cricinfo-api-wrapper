from app.main import *
from http_constants.headers import HttpHeaders
import unittest

TEST_SERVER = 'http://localhost:5000'
TEST_SERVER_PLAYER_HOME_PATH = TEST_SERVER + PLAYER_HOME_PATH
TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH = TEST_SERVER + PLAYER_HOME_PATH_WITH_SLASH
PLAYER_ID = "28081"  # MS Dhoni
INVALID_PLAYER_ID_STRING = "INVALID_ID"
INVALID_PLAYER_ID = "999999999"
CHAR_SET = '; charset=utf-8'


def check_for_response_with_text(self, res, msg, status_code):
    self.assertEqual(status_code, res.status_code)
    self.assertEqual(HttpHeaders.CONTENT_TYPE_VALUES.html + CHAR_SET, res.content_type)
    self.assertEqual(msg, str(res.data.decode("utf-8")))


def check_for_200_with_json(self, res):
    self.assertEqual(200, res.status_code)
    self.assertEqual(HttpHeaders.CONTENT_TYPE_VALUES.json, res.content_type)


class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.test_client = app.test_client()

    def test_server_up_and_running(self):
        """ Test that the flask server is running and reachable"""
        r = self.test_client.get(TEST_SERVER + "/")
        check_for_response_with_text(self, r, HOME_MSG, 200)

    def test_player_home(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH)
        check_for_response_with_text(self, r, PLAYER_HOME_MSG, 200)

    def test_player_home_with_slash(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH)
        check_for_response_with_text(self, r, PLAYER_HOME_MSG, 200)

    def test_get_summary(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + PLAYER_ID)
        check_for_200_with_json(self, r)
        self.assertEqual(2383, r.content_length)
        player = r.json
        self.assertEqual('Mahendra Singh Dhoni', player['fullName'])
        self.assertEqual('1981-07-07T00:00Z', player['dob'])
        self.assertEqual(64914, player['odiDebut']['match_id'])
        self.assertEqual('Bangladesh v India at Chattogram, Dec 23, 2004', player['odiDebut']['title'])
        self.assertEqual(226361, player['testDebut']['match_id'])
        self.assertEqual('India v Sri Lanka at Chennai, Dec 2-6, 2005', player['testDebut']['title'])
        self.assertEqual(255954, player['t20iDebut']['match_id'])
        self.assertEqual('South Africa v India at Johannesburg, Dec 1, 2006', player['t20iDebut']['title'])

    def test_get_summary_for_invalid_id(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID_STRING)
        check_for_response_with_text(self, r, ERR_DONT_ACT_SMART_VALID_ID, 400)

    def test_get_summary_for_player_not_found(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID)
        check_for_response_with_text(self, r, ERR_PLAYER_NOT_FOUND, 404)

    def test_get_batting_stats(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + PLAYER_ID + BATTING_PATH)
        check_for_200_with_json(self, r)
        self.assertEqual(1487, r.content_length)
        player = r.json
        self.assertEqual('12303', player['ODIs']['balls_faced'])
        self.assertEqual('123', player['ODIs']['stumpings'])
        self.assertEqual('50.57', player['ODIs']['batting_average'])
        self.assertEqual('87.56', player['ODIs']['strike_rate'])
        self.assertEqual('8249', player['Tests']['balls_faced'])
        self.assertEqual('38', player['Tests']['stumpings'])
        self.assertEqual('38.09', player['Tests']['batting_average'])
        self.assertEqual('59.11', player['Tests']['strike_rate'])
        self.assertEqual('1282', player['T20Is']['balls_faced'])
        self.assertEqual('34', player['T20Is']['stumpings'])
        self.assertEqual('37.60', player['T20Is']['batting_average'])
        self.assertEqual('126.13', player['T20Is']['strike_rate'])

    def test_get_batting_stats_for_invalid_id(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID_STRING + BATTING_PATH)
        check_for_response_with_text(self, r, ERR_DONT_ACT_SMART_VALID_ID, 400)

    def test_get_batting_stats_for_player_not_found(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID + BATTING_PATH)
        check_for_response_with_text(self, r, ERR_PLAYER_NOT_FOUND, 404)

    def test_get_bowling_stats(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + PLAYER_ID + BOWLING_PATH)
        check_for_200_with_json(self, r)
        self.assertEqual(1454, r.content_length)
        player = r.json
        self.assertEqual('36', player['ODIs']['balls_delivered'])
        self.assertEqual('1/14', player['ODIs']['best_innings'])
        self.assertEqual('31.00', player['ODIs']['bowling_average'])
        self.assertEqual('5.16', player['ODIs']['economy'])
        self.assertEqual('31', player['ODIs']['runs'])
        self.assertEqual('36.0', player['ODIs']['strike_rate'])
        self.assertEqual('1', player['ODIs']['wickets'])
        self.assertEqual('96', player['Tests']['balls_delivered'])
        self.assertEqual('-', player['Tests']['best_innings'])
        self.assertEqual('4.18', player['Tests']['economy'])
        self.assertEqual('67', player['Tests']['runs'])
        self.assertEqual('0', player['Tests']['wickets'])
        self.assertEqual('-', player['T20Is']['balls_delivered'])

    def test_get_bowling_stats_for_invalid_id(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID_STRING + BOWLING_PATH)
        check_for_response_with_text(self, r, ERR_DONT_ACT_SMART_VALID_ID, 400)

    def test_get_bowling_stats_for_player_not_found(self):
        r = self.test_client.get(TEST_SERVER_PLAYER_HOME_PATH_WITH_SLASH + INVALID_PLAYER_ID + BOWLING_PATH)
        check_for_response_with_text(self, r, ERR_PLAYER_NOT_FOUND, 404)


if __name__ == '__main__':
    unittest.main()
