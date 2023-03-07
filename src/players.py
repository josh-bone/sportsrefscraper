import pandas as pd
from bs4 import BeautifulSoup
from .utils import HttpRequest, player_suffix

# def get_game_logs(playername, _type='per_game', playoffs=False):
#     if playoffs:
#         _type = 'playoffs_' + _type
#     suffix = player_suffix(playername).replace('/', '%2F')
    
#     # # WARNING: widgets has been retired as of Jan 1, 2023!
#     # query_url = f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{_type}'
#     # # TODO: find a new place to scrape game logs 
    
#     resp = HttpRequest.get(query_url)
#     if resp.status_code==200:
#         soup = BeautifulSoup(resp.content, 'html.parser')
        
#         att = {'id': 'pgl_basic_playoffs'} if playoffs else {'id': 'pgl_basic'}
#         table = soup.find('table', attrs=att)
#         if table:
#             df = pd.read_html(str(table))[0]
#             df.rename(columns = {'Date': 'DATE', 'Age': 'AGE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
#                 'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE'}, inplace=True)
#             df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
#             df = df[df['Rk'] != 'Rk']
#             df = df.drop(['Rk', 'G'], axis=1)
#             df['DATE'] = pd.to_datetime(df['DATE'])
#             df = df[df['GS'] == '1'].reset_index(drop=True)
#             return df
#         else:
#             # htmlname = "game_log_request.html"
#             # print(f"Dumping to {htmlname}")
#             # with open(htmlname, "w") as file:
#             #     file.write(str(soup))
#             raise ValueError(f"Table not found")
#     else:
#         raise ValueError(f"Request failed with status code {resp.status_code}")