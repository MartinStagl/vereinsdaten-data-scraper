from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def process_player(soup: BeautifulSoup):
    player = {}
    try:
        player["name"] = soup[0].select('a')[0]["title"]
        player["position"] = soup[1].select('.c2 .m_g_text_1')[0].text
        player["goals"] = soup[3].text.strip()
        player["yellow_cards"] = soup[4].text.strip()
        player["red_cards"] = soup[6].text.strip()
        player["url"] = soup[0].select('.c1 a')[0]['href']
    except:
        print(*soup)
    return player

class MatchScraper():

    driver=None

    def __init__(self,driver,url = 'https://www.oefb.at/bewerbe/Spiel/Aufstellung/3172013/?Sigless-2-Kl-Cup-A-vs-Grosshoeflein-2-N-',search_term='Aufstellung'):
        self.driver=driver
        self.driver.implicitly_wait(60)
        print("Querying url {}".format(url.replace("Spielbericht",search_term)))
        self.driver.get(url.replace("Spielbericht",search_term))

    def get_data(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        print(soup.prettify("utf-8"))
        with open("game.html", "w") as file:
            file.write(str(soup))
        # print(soup.prettify("utf-8"))

        data = {}
        # print(soup.prettify("utf-8"))
        data["url"]=self.driver.current_url
        data["date"] = soup.select('div .date ')[0].text
        data["starttime"] = soup.select('div.detail > div:nth-child(3) > div:nth-child(1) > span:nth-child(2)')[0].text
        data["league"] = soup.select('div.detail > div:nth-child(1) > span:nth-child(2)')[0].text
        data["round"] = soup.select('div.detail > div:nth-child(1) > span:nth-child(3)')[0].text
        data["result"] = soup.select('.ergebnis')[0].text
        data["home_team_name"] = soup.select('div > div.teams > a:nth-child(2)')[0].text.strip()
        data["away_team_name"] = soup.select('div > div.teams > a:nth-child(3)')[0].text.strip()

        data["home_players"] = [process_player(item) for item in zip(*[iter(soup.select(
            'div[data-heimaufstellung] .c1,div[data-heimaufstellung] .c2,div[data-heimaufstellung] .c3,div[data-heimaufstellung] .c4,div[data-heimaufstellung] .c5,div[data-heimaufstellung] .c6,div[data-heimaufstellung] .c7,div[data-heimaufstellung] .c8'))] * 8)]
        data["away_players"] = [process_player(item) for item in zip(*[iter(soup.select(
            'div[data-gastaufstellung] .c1,div[data-gastaufstellung] .c2,div[data-gastaufstellung] .c3,div[data-gastaufstellung] .c4,div[data-gastaufstellung] .c5,div[data-gastaufstellung] .c6,div[data-gastaufstellung] .c7,div[data-gastaufstellung] .c8'))] * 8)]
        json.dumps(data, indent=4)
        return data




