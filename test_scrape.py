"""test_scrape.py
"""

import datetime as dt
# import sportsrefscraper as srs
from sportsrefscraper.players import scrape_game_logs, scrape_per100
from sportsrefscraper.games import scrape_boxscores, scrape_play_by_play, scrape_shot_chart
from sportsrefscraper.teams import get_roster
from sportsrefscraper.config import TEAMNAME_TO_ID, PLAYERS
import random

GAMES = [
        [dt.date(2023, 3, 4), 'PHI', 'MIL']
    ]

class TestScrape:
    
    def test_gamelogs(self):
        player = random.choice(PLAYERS)
        assert scrape_game_logs(player) is not None
        
    def test_pbp(self):
        game = random.choice(GAMES)
        day, t1, t2 = game
        assert scrape_play_by_play(day, t1, t2) is not None
        
    def test_boxcores(self):
        game = random.choice(GAMES)
        day, t1, t2 = game
        assert scrape_boxscores(day, t1, t2) is not None
        
    def test_shot_chart(self):
        game = random.choice(GAMES)
        day, t1, t2 = game
        assert scrape_shot_chart(day, t1, t2) is not None
        
    def test_roster(self):
        team = random.choice(list(TEAMNAME_TO_ID.values()))
        assert get_roster(team, 2023) is not None
        
    def test_per100(self):
        player = random.choice(PLAYERS)
        assert scrape_per100(player) is not None