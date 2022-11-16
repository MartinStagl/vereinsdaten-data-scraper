
from bs4 import BeautifulSoup


class MatchFinder():
    driver = None

    def __init__(self,driver,
                 url='https://www.oefb.at/bewerbe/Spiel/Aufstellung/3172013/'):
        self.driver=driver
        self.driver.implicitly_wait(60)
        self.driver.get(url)

    def getMatches(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        matches_raw=soup.select('#spielplan td.status > a', href=True)
        match_urls =  [a['href'] for a in matches_raw ]
        print(*match_urls,sep="\n")
        return match_urls

    def getLeagueUrls(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        urls = set()
        urls.update(a['href'] for a in soup.select("#navigation  span.label > a",href=True))
        return urls


