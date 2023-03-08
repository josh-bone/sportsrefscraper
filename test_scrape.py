import datetime as dt
from sportsrefscraper.players import scrape_game_logs
from sportsrefscraper.games import scrape_boxscores, scrape_play_by_play, scrape_shot_chart

class TestScrape:
    
    def test_gamelogs(self):
        assert scrape_game_logs('Joel Embiid') is not None
        
    def test_pbp(self):
        assert scrape_play_by_play(dt.date(2023, 3, 4), 'PHI', 'MIL') is not None
        
    def test_boxcores(self):
        assert scrape_boxscores(dt.date(2023, 3, 4), 'PHI', 'MIL') is not None
        
    def test_shot_chart(self):
        assert scrape_shot_chart(dt.date(2023, 3, 4), 'PHI', 'MIL') is not None