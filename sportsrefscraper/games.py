from .utils import HttpRequest, get_game_suffix
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import re


def scrape_boxscores(date, away, home):
    suffix = get_game_suffix(date, away, home)
    query_url = f"https://www.basketball-reference.com{suffix}"
    sesh = HttpRequest()
    resp = sesh.get(query_url)
    
    basic_stats = {}
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # four_factors = soup.find('table', attrs={'id': f'four_factors'})
        # ff_df = pd.read_html(str(four_factors))[0]
        
        away_table = soup.find('table', attrs={'id': f'box-{away}-game-basic'})
        away_basic = pd.read_html(str(away_table))[0]
        home_table = soup.find('table', attrs={'id': f'box-{home}-game-basic'})
        home_basic = pd.read_html(str(home_table))[0]
        
        basic_stats[away] = away_basic
        basic_stats[home] = home_basic
        # basic_stats['four_factors'] = ff_df
    else:
        raise ValueError(f"Response failed with code {resp.status_code}")
    
    return basic_stats


def scrape_shot_chart(date, away, home):
    """Scrapes basketball-reference.com for shot charts

    Args:
        date (datetime object): _description_
        away (str): away team
        home (str): home team

    Raises:
        ValueError: if response returns anything but status code 200

    Returns:
        _type_: dictionary indexed by the team
    """    
    suffix = get_game_suffix(date, away, home).replace('/boxscores', '')  # e.g. 202303040MIL
    sesh = HttpRequest()
    query_url = f'https://www.basketball-reference.com/boxscores/shot-chart{suffix}'
    resp = sesh.get(query_url)
    
    ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/shot_charts.py
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        id_away = f'shots-{away}'
        id_home = f'shots-{home}'
        away_div = soup.find('div', attrs={'id': id_away})
        home_div = soup.find('div', attrs={'id': id_home})
        
        df1 = pd.DataFrame()
        for div in away_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df1 = pd.concat([df1, shot_df])
        df1 = df1.reset_index()
        df1 = df1.drop('index', axis=1)
        
        df2 = pd.DataFrame()
        for div in home_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df2 = pd.concat([df2, shot_df])
        df2 = df2.reset_index()
        df2 = df2.drop('index', axis=1)

        return {f'{away}': df1, f'{home}': df2}
    else:
        raise ValueError(f"Request failed with status code {resp.status_code}")
    
def scrape_play_by_play(date, team1, team2):
    """Scrapes basketball-reference.com for the play-by-play

    Args:
        date (datetime object): date of game
        team1 (str): 3-letter teamname abbreviation (uppercase)
        team2 (str): 3-letter teamname abbreviation of the other team (uppercase)

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """    
    suffix = get_game_suffix(date, team1, team2)
    assert suffix is not None
    suffix = suffix.replace('/boxscores', '')
    
    # selector = f'#pbp'
    resp = HttpRequest().get(f'https://www.basketball-reference.com/boxscores/pbp{suffix}')
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        df = pd.read_html(str(table))[0]
    else:
        raise ValueError(f"Response failed with code {resp.status_code}")
    
    df = format_pbp(df)
    return df

def format_pbp(pbp_df):
    pbp_df.columns = list(map(lambda x: x[1], list(pbp_df.columns)))
    t1 = list(pbp_df.columns)[1].upper()
    t2 = list(pbp_df.columns)[5].upper()
    q = 1
    df = None
    for index, row in pbp_df.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row['Time']=='2nd Q':
            q = 2
        elif row['Time']=='3rd Q':
            q = 3
        elif row['Time']=='4th Q':
            q = 4
        elif 'OT' in row['Time']:
            q = row['Time'][0]+'OT'
        try:
            d['QUARTER'] = q
            d['TIME_REMAINING'] = row['Time']
            scores = row['Score'].split('-')
            d[f'{t1}_SCORE'] = int(scores[0])
            d[f'{t2}_SCORE'] = int(scores[1])
            d[f'{t1}_ACTION'] = row[list(pbp_df.columns)[1]]
            d[f'{t2}_ACTION'] = row[list(pbp_df.columns)[5]]
            if df is None:
                df = pd.DataFrame(columns = list(d.keys()))
            df = pd.concat([df, d], ignore_index=True)
        except:
            continue
    return df
    
def get_location(s):
    ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/shot_charts.py#L11
    l = s.split(';')
    top = float(l[0][l[0].index(':')+1:l[0].index('px')])
    left = float(l[1][l[1].index(':')+1:l[1].index('px')])
    x = left/500.0*50
    y = top/472.0*(94/2)
    return {'x': str(x)[:4] + ' ft', 'y': str(y)[:4] + ' ft'}

def get_description(s):
    ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/shot_charts.py#L11
    match = re.match(r'(\d)[a-z]{2} quarter, (\S*) remaining<br>(.*) \b(missed|made) (\d)-pointer from (\d*) ft', s)
    d = {}
    if match:
        groups = match.groups()
        d['QUARTER'] = int(groups[0])
        d['TIME_REMAINING'] = groups[1]
        d['PLAYER'] = groups[2]
        d['MAKE_MISS'] = 'MAKE' if groups[3]=='made' else 'MISS'
        d['VALUE'] = int(groups[4])
        d['DISTANCE'] = groups[5] + ' ft'
    return d