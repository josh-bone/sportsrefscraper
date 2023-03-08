from utils import HttpRequest
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt

def nba_schedule(season_end_year=None):
    """Scrapes basketball-reference.com for the requested year's schedule

    Args:
        season_end_year (str): the year that the requested season ended

    Raises:
        ValueError: If the HTTP request fails
    """    
    
    # TODO: check that this sets the correct year... I think the season ends in July
    if season_end_year is None:
        now = dt.now()
        season_end_year = now.year if now.month < 7 else now.year+1
    
    if type(season_end_year) == str:
        season_end_year = int(season_end_year)
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May', 'June']
    if season_end_year == 2020:
        # League took a break due to the COVID-19 pandemic
        months = ['October-2019', 'November', 'December', 'January', 'February', 'March',
                'July', 'August', 'September', 'October-2020']
        
    season_df = pd.Dataframe()
    sesh = HttpRequest()
    for month in months:
        query_url = f'https://www.basketball-reference.com/leagues/NBA_{season_end_year}_games-{month.lower()}.html'
        resp = sesh.get(query_url)
        assert resp is not None, "HTTPS returned None"
        if resp.status_code==200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            if table:
                month_df = pd.read_html(str(table))[0]
                season_df = pd.concat([season_df, month_df],ignore_index=True,axis=0)
        else:
            raise ValueError(f"Request failed with status code {resp.status_code}")

    return(season_df)

    
def nba_standings(date=None):
    """Returns the NBA standings as of the requested date. If no date is provided, it gets the current standings.

    Args:
        date (datetime object, optional): The date for which to fetch NBA standings. Defaults to None.

    Raises:
        ValueError: If reading the data was unsuccessful
    """    
    if date is None:
        date = dt.now()
    
    query_url = f'https://www.basketball-reference.com/friv/standings.fcgi?month={date.month}&day={date.day}&year={date.year}'
    resp = HttpRequest().get(query_url)
    
    standings = {}
    
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        e_table = soup.find('table', attrs={'id': 'standings_e'})
        w_table = soup.find('table', attrs={'id': 'standings_w'})
        if e_table and w_table:
            e_df = pd.read_html(str(e_table))[0]
            w_df = pd.read_html(str(w_table))[0]
            e_df.rename(columns={'Eastern Conference': 'TEAM'}, inplace=True)
            w_df.rename(columns={'Western Conference': 'TEAM'}, inplace=True)
        else:
            raise ValueError("Failed to read the standings tables")
        standings['East'] = e_df
        standings['West'] = w_df
    else:
        raise ValueError(f"Request failed with status code {resp.status_code}")