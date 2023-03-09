# from .utils import 
import pandas as pd
from bs4 import BeautifulSoup
from .utils import HttpRequest, teamname_to_id

def get_roster(team, season_end_year):
    
    if len(team) > 3 : team = teamname_to_id(team)
    
    query_url = f'https://www.basketball-reference.com/teams/{team.upper()}/{season_end_year}.html'
    resp = HttpRequest().get(query_url)
    
    ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/teams.py
    df = None
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                      'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
        # remove rows with no player name (this was the issue above)
        df = df[df['PLAYER'].notna()]
        
        ## TODO: handle players with atypical characters in their name: i.e....
        # df['PLAYER'] = df['PLAYER'].apply(
        #     lambda name: remove_accents(name, team, season_end_year))
        
        # handle rows with empty fields but with a player name.
        df['BIRTH_DATE'] = df['BIRTH_DATE'].apply(
            lambda x: pd.to_datetime(x) if pd.notna(x) else pd.NaT)
        df['NATIONALITY'] = df['NATIONALITY'].apply(
            lambda x: x.upper() if pd.notna(x) else '')
    else:
        raise ValueError(f"HTML request failed with status code {resp.status_code}")

    return df
