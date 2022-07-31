from selenium import webdriver
from bs4 import BeautifulSoup

class MatchScraper():

    driver=None

    def __init__(self,url = 'https://www.oefb.at/bewerbe/Spiel/Aufstellung/3172013/?Sigless-2-Kl-Cup-A-vs-Grosshoeflein-2-N-',search_term='Aufstellung'):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(60)
        print("Querying url {}".format(url.replace("Spielbericht",search_term)))
        self.driver.get(url.replace("Spielbericht",search_term))


    def getPlayers(self):
        html=self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        #print(soup.prettify("utf-8"))
        player_raw=soup.select('.m_g_player_1')
        print(*player_raw)
        return player_raw


