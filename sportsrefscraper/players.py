import pandas as pd
from bs4 import BeautifulSoup
from .utils import HttpRequest, player_suffix
import datetime as dt

def scrape_game_logs(playername, year=None, _type='per_game'):
    if year is None:
        year = dt.datetime.now().year
    suffix = player_suffix(playername).strip('.html') + f'/gamelog/{year}'
    
    query_url = f'https://www.basketball-reference.com{suffix}'  # e.g. https://www.basketball-reference.com/players/i/irvinky01/gamelog/2023
    id = 'pgl_basic'
    
    resp = HttpRequest().get(query_url)
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        att = {'id': 'pgl_basic'}
        table = soup.find('table', attrs=att)
        if table:
            df = pd.read_html(str(table))[0]
            df.rename(columns = {'Date': 'DATE', 'Age': 'AGE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
                'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE'}, inplace=True)
            df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
            df = df[df['Rk'] != 'Rk']
            df = df.drop(['Rk', 'G'], axis=1)
            df['DATE'] = pd.to_datetime(df['DATE'])
            df = df[df['GS'] == '1'].reset_index(drop=True)
            return df
        else:
            # htmlname = "game_log_request.html"
            # print(f"Dumping to {htmlname}")
            # with open(htmlname, "w") as file:
            #     file.write(str(soup))
            raise ValueError(f"Table not found")
    else:
        raise ValueError(f"Request failed with status code {resp.status_code}")