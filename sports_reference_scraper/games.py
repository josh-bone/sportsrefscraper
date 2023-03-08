from .utils import HttpRequest, get_game_suffix
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
import re


def scrape_shot_chart(date, away, home):
    """TODO: NOT TESTED YET

    Args:
        date (datetime object): _description_
        away (str): away team
        home (str): home team

    Raises:
        ValueError: if response returns anything but status code 200

    Returns:
        _type_: dictionary indexed by the team
    """    
    suffix = get_game_suffix(date, away, home).replace('/boxscores', '')
    sesh = HttpRequest()
    query_url = f'https://www.basketball-reference.com/boxscores/shot-chart{suffix}'
    resp = sesh.get(query_url)
    
    ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/shot_charts.py
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        shot_chart1_div = soup.find('div', attrs={'id': f'shots-{away}'})
        shot_chart2_div = soup.find('div', attrs={'id': f'shots-{home}'})
        df1 = pd.DataFrame()
        for div in shot_chart1_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df1 = df1.append(shot_df)
        df1 = df1.reset_index()
        df1 = df1.drop('index', axis=1)
        df2 = pd.DataFrame()
        for div in shot_chart2_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df2 = df2.append(shot_df)
        df2 = df2.reset_index()
        df2 = df2.drop('index', axis=1)

        return {f'{away}': df1, f'{home}': df2}
    else:
        raise ValueError(f"Request failed with status code {resp.status_code}")
    
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