from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import traceback

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

def process_activity(soup: BeautifulSoup):
    activity = {}
    activity["text"]= ""
    activity["team"] = ""
    activity["player"]= ""
    activity["minute"]= ""
    activity["standing"]= ""
    activity["substitution_player"]= ""
    activity["type"]= ""
    try:
        activity["minute"] = soup[2].text.strip()
        if len(soup[0].select('a')) > 0:
            activity["team"] = "home"
            activity["player"] = soup[0].select('a')[0]['href']
            if str(soup[1].select('img')[0]["title"]).lower() == "tor":
                activity["standing"] = soup[0].select('.highlight')[0].text.strip()
                activity["type"] = "goal"
                activity["text"] = soup[0].select('span')[0].text.strip()
            elif str(soup[1].select('img')[0]["title"]).lower() == "gelbe karte":
                activity["type"] = "yellow card"
                activity["text"] = soup[0].select('span')[0].text.strip()
            elif str(soup[1].select('img')[0]["title"]).lower() == "rote karte":
                activity["type"] = "red card"
                activity["text"] = soup[0].select('span')[0].text.strip()
            elif str(soup[1].select('img')[0]["title"]).lower() == "wechsel":
                activity["substitution_player"] = soup[0].select('a')[1]['href']
                activity["type"] = "substitution"

        if len(soup[4].select('a')) > 0:
            activity["team"] = "away"

            activity["player"] = soup[4].select('a')[0]['href']
            if str(soup[3].select('img')[0]["title"]).lower() == "tor":
                activity["standing"] = soup[4].select('.highlight')[0].text.strip()
                activity["type"] = "goal"
                activity["text"] = soup[4].select('span')[0].text.strip()
            elif str(soup[3].select('img')[0]["title"]).lower() == "gelbe karte":
                activity["type"] = "yellow card"
                activity["text"] = soup[4].select('span')[0].text.strip()
            elif str(soup[3].select('img')[0]["title"]).lower() == "rote karte":
                activity["type"] = "red card"
                activity["text"] = soup[4].select('span')[0].text.strip()
            elif str(soup[3].select('img')[0]["title"]).lower() == "wechsel":
                activity["substitution_player"] = soup[4].select('a')[1]['href']
                activity["type"] = "substitution"


    except:
        print(traceback.format_exc())
    return activity

class MatchScraper():

    driver=None
    url=None
    def __init__(self,driver,url = 'https://www.oefb.at/bewerbe/Spiel/Aufstellung/3172013/?Sigless-2-Kl-Cup-A-vs-Grosshoeflein-2-N-'):
        self.driver=driver
        self.driver.implicitly_wait(60)
        self.url=url

    def get_formation(self,search_term='Aufstellung'):
        print("Querying url {}".format(self.url.replace("Spielbericht", search_term)))
        self.driver.get(self.url.replace("Spielbericht", search_term))

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        #print(soup.prettify("utf-8"))
        with open("game.html", "w") as file:
            file.write(str(soup))
        # print(soup.prettify("utf-8"))

        data = {}
        # print(soup.prettify("utf-8"))
        data["url"]=self.driver.current_url
        data["date"] = soup.select('div .date ')[0].text
        data["starttime"] = soup.select('div.detail > div:nth-child(3) > div:nth-child(1) > span:nth-child(2)')[0].text
        data["league"] = soup.select('div.detail > div:nth-child(1) > span:nth-child(2)')[0].text
        data["round"] = soup.select('div > div.round')[0].text
        data["result"] = soup.select('.ergebnis')[0].text

        data["home_team_name"] = soup.select('div > div.teams > a:nth-child(2)')[0].text.strip()
        data["away_team_name"] = soup.select('div > div.teams > a:nth-child(3)')[0].text.strip()

        data["home_team_trainer"]= soup.select('.person_box_short_1 > span')[0].text.replace("Trainer:","").strip()
        data["away_team_trainer"] = soup.select('.person_box_short_1 > span')[2].text.replace("Trainer:","").strip()

        data["home_players"] = [process_player(item) for item in zip(*[iter(soup.select(
            'div[data-heimaufstellung] .c1,div[data-heimaufstellung] .c2,div[data-heimaufstellung] .c3,div[data-heimaufstellung] .c4,div[data-heimaufstellung] .c5,div[data-heimaufstellung] .c6,div[data-heimaufstellung] .c7,div[data-heimaufstellung] .c8'))] * 8)]
        data["away_players"] = [process_player(item) for item in zip(*[iter(soup.select(
            'div[data-gastaufstellung] .c1,div[data-gastaufstellung] .c2,div[data-gastaufstellung] .c3,div[data-gastaufstellung] .c4,div[data-gastaufstellung] .c5,div[data-gastaufstellung] .c6,div[data-gastaufstellung] .c7,div[data-gastaufstellung] .c8'))] * 8)]
        json.dumps(data, indent=4)
        return data

    def get_activities(self,search_term='Spielbericht'):
        print("Querying url {}".format(self.url.replace("Spielbericht", search_term)))
        self.driver.get(self.url.replace("Spielbericht", search_term))

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        data = {}
        data["activities"] = [process_activity(item) for item in
                              zip(*[iter(soup.select('div.game_report_by_events_grid_2 > div'))] * 5)]
        return data




