import pandas as pd
import unidecode  # TODO: may need this

from sys import stderr
from requests import Session as HttpSession
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup

from .config import TEAMNAME_TO_ID


class HttpRequest:
    __session = None

    @staticmethod
    def __init__session__():
        if HttpRequest.__session is not None:
            return
        stderr.write("Initializing HTTPS Session\n")
        HttpRequest.__session = HttpSession()
        retries = Retry(total=10,
                        backoff_factor=1,
                        status_forcelist=[429],
                        allowed_methods=False)
        HttpRequest.__session.mount("https://", HTTPAdapter(max_retries=retries))

    @staticmethod
    def get(url):
        print(f"Querying {url}")
        HttpRequest.__init__session__()
        return HttpRequest.__session.get(url)

def player_suffix(_name):
    bothnames = _name.lower().split(' ')
    firstname = bothnames[0]
    firstname_code = firstname[:2]
    
    if len(bothnames[1]) > 5: lastname_code = bothnames[1][:5]
    else: lastname_code = bothnames[1]
    
    last_initial = bothnames[1][0]
    
    suffix = '/players/'+ last_initial + '/' + lastname_code + firstname_code + '01.html'
    resp = HttpRequest.get(f'https://www.basketball-reference.com{suffix}')
        
    while resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        ## https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/utils.py#L51
        header = soup.find('h1')
        if header:
            page_name = header.find('span').text
            if ((unidecode.unidecode(page_name)).lower() == _name):
                # the URL we constructed matches the name of the player on this page
                return suffix
            else:
                # Try another one
                all_names = unidecode.unidecode(page_name).lower().split(' ')
                page_first_name = all_names[0]
                if firstname == page_first_name.lower():
                    return suffix
                # if players have same first two letters of last name then just increment suffix
                elif firstname[:2] == page_first_name.lower()[:2]:
                    player_number = int(''.join(c for c in suffix if c.isdigit())) + 1
                    # if player_number < 10:
                    #     player_number = f"0{str(player_number)}"
                    suffix = f"/players/{last_initial}/{lastname_code}{firstname_code}{player_number:02d}.html"
                
                resp = HttpRequest.get(f'https://www.basketball-reference.com{suffix}')
        ##
        
    if resp.status_code != 200:
        raise ValueError(f"{resp.status_code}")
    
    
def teamname_to_id(fullname):
    assert type(fullname) == str, f'Improper teamname format: {type(fullname)}'
    fullname = fullname.upper().replace('-', ' ')
    abbrev = TEAMNAME_TO_ID[fullname]
    return(abbrev)

def get_game_suffix(date, team1, team2):
    """
    (Taken from https://github.com/josh-bone/basketball_reference_scraper/blob/master/src/utils.py)

    Args:
        date (datetime object): _description_
        team1 (_type_): _description_
        team2 (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """    
    print(f"Searching for {team1} or {team2}")
    
    _url = f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}'
    print(f"Querying {_url}")
    resp = HttpRequest().get(_url)
    
    suffix = None
    
    if resp.status_code==200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        tables = soup.find_all('table', attrs={'class': 'teams'})
        # print(f"Found {len(tables)} tables")
        for i,table in enumerate(tables):
            a_list = table.find_all('a')
            # print(f"\nTable {i} has {len(a_list)} a's")
            for anchor in a_list:
                # print(f"anchor.attrs['href'] is {anchor.attrs['href']}")
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    else: 
        raise ValueError(resp.status_code)
    return suffix