from .utils import HttpRequest
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt


def scrape_team_vs_team(year=None, month=None):
    """Scrape the record of each team against each other team - returned in a pandas DataFrame

    Args:
        year (int): the calendar year 
        month (str): the month for which to scrape the schedule. If None, returns the schedule for all months.

    Raises:
        ValueError: If reading the data was unsuccessful
    """    
    try:
        now = dt.now()
    except:
        now = dt.datetime.now()
    
    if year is None:
        year = now.year
    
    if type(year) == str:
        year = int(year)
        
    assert type(month) == str
        
    id = 'team_vs_team'
    atts = {'id': id}
    
    sesh = HttpRequest()
    query_url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month.lower()}.html'
    resp = sesh.get(query_url)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table', attrs=atts)
        if table:
            df = pd.read_html(str(table))[0]
            return(df)
        else:
            raise ValueError(f"Failed to find table at {query_url}")
    else:
        raise ValueError(f"Http Response at {query_url}\n\tfailed with status code {resp.status_code}")
    
def nba_schedule(year=None, month=None):
    """Scrapes basketball-reference.com for the requested year's schedule

    Args:
        year (int): the calendar year 
        month (str): the month for which to scrape the schedule. If None, returns the schedule for all months.

    Raises:
        ValueError: If the HTTP request fails
    """    
    
    try:
        now = dt.now()
    except:
        now = dt.datetime.now()
        
    if year is None:
        year = now.year
    
    if type(year) == str:
        year = int(year)
        
    valid_months = ['january', 'february', 'march',
            'april', 'may', 'june', 'october', 'november', 'december']
    if month is None:
        sched = pd.DataFrame()
        for ind, m in enumerate(valid_months):
            cur = nba_schedule(year=year, month=m)
            sched = pd.concat([sched, cur], axis=0, ignore_index=True)
            if ind + 1 == now.month:
                break
        return(sched)
    assert month in valid_months, f"Improper month argument: {month}"
    
    if month == 'october':
        if year == 2019:
            # League took a break due to the COVID-19 pandemic
            month = 'October-2019'
        elif year == 2020:
            month = 'October-2020'
        
    sesh = HttpRequest()
    query_url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'
    resp = sesh.get(query_url)
    assert resp is not None, "HTTPS returned None"
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'schedule'})
        if table:
            month_df = pd.read_html(str(table))[0]
    else:
        raise ValueError(f"Request failed with status code {resp.status_code}")

    return(month_df)

    
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
    sesh = HttpRequest()
    resp = sesh.get(query_url)
    
    standings = None
    
    if resp.status_code==200:
        standings = {}
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
    
    return(standings)