import requests
from bs4 import BeautifulSoup

def check_for_updates(config):
    if config['update_check'] == "True":
        version = config['version']
        url = "https://github.com/LunaLimpets/Inara_StreamDeck_Connector/releases"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, features="lxml")
            releases = soup.find_all('span', {'class':'ml-1 wb-break-all'})
            if releases[0].text.strip() != version:
                return True
            else:
                return False    
