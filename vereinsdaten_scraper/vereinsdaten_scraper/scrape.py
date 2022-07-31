from scraper.selenium_match_scraper import *
from scraper.selenium_match_finder import *



def to_database(players_raw):
    print(*players_raw)

if __name__ == "__main__":
    start_url="https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/BFV-2Klasse-2Nord/Spielplan/aktuell/2008"
    matches=set()
    # Match finder Thread:
    # Find matches to scrape and write to database
    matches.update(MatchFinder(start_url).getMatches())
    print("Successfully found {} matches".format(len(matches)))
    # Match data scraper Thread
    # Scrape Data from Matches and save to Database
    url=matches.pop()
    to_database(MatchScraper(url).getPlayers())

    print("DONE")