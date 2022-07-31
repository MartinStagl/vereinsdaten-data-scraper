from selenium import webdriver
from bs4 import BeautifulSoup


class MatchFinder():
    driver = None

    def __init__(self,
                 url='https://www.oefb.at/bewerbe/Spiel/Aufstellung/3172013/?Sigless-2-Kl-Cup-A-vs-Grosshoeflein-2-N-/aufstellung'):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(60)
        self.driver.get(url)

    def getMatches(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        matches_raw=soup.select('#spielplan td.status > a', href=True)
        match_urls =  [a['href'] for a in matches_raw ]
        print(*match_urls,sep="\n")
        return match_urls


