from scraper.selenium_match_scraper import *
from scraper.selenium_match_finder import *

from selenium import webdriver
import traceback
from dao.setup import *
import dao.database_connector as dbc


from datetime import datetime

def to_database(data):
    m = Match()
    m.url = data["url"]
    m.date = datetime.strptime(data["date"], "%d.%m.%Y")
    m.starttime = data["starttime"]
    m.league = data["league"]
    m.round = data["round"]
    m.result = data["result"]

    home_team=dbc.get_or_insert_team(data["home_team_name"])
    away_team=dbc.get_or_insert_team(data["away_team_name"])

    for player in data["home_players"]:
        p = dbc.get_or_insert_player(player["url"])
        p.name= player["name"]
        #p.birthyear=player["birthyear"]
        #p.nationality = player["nationality"]
        mp=MatchPlayer()
        mp.player=p
        mp.goals=player["goals"]
        mp.position = player["position"]
        mp.red_cards = player["red_cards"]
        mp.yellow_cards = player["yellow_cards"]
        #mp.starting_minute = player["starting_minute"]
        #mp.substitution_player = player["substitution_player"]
        #mp.substitution_minute = player["substitution_minute"]
        #home_team.players.append(p)
        dbc.insert_player(p)
        m.players.append(mp)

        #home_team.players.append(player)

    for player in data["away_players"]:
        p = dbc.get_or_insert_player(player["url"])
        p.name= player["name"]
        #p.birthyear=player["birthyear"]
        #p.nationality = player["nationality"]
        mp=MatchPlayer()
        mp.player=p
        mp.goals=player["goals"]
        mp.position = player["position"]
        mp.red_cards = player["red_cards"]
        mp.yellow_cards = player["yellow_cards"]
        #mp.starting_minute = player["starting_minute"]
        #mp.substitution_player = player["substitution_player"]
        #mp.substitution_minute = player["substitution_minute"]
        dbc.insert_player(p)
        m.players.append(mp)
        #away_team.players.append(p)

    m.away_team = away_team
    m.home_team = home_team

    dbc.insert(m,home_team,away_team)


if __name__ == "__main__":
    #start_url="https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/BFV-2KL-2N/Spielplan/aktuell/{}"
    base_url="https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/{}/Spielplan/aktuell/{}"
    leagues=["BFV-Regionalligen-RegionalligaOst",
            "BFV-BVZBurgenlandliga-BVZBurgenlandliga","BFV-BL-BurgenlandligaReserve",
          "BFV-IILigen-IILigaNord","BFV-IILiga-IILigaMitte","BFV-IILigen-IILigaSued",
            "BFV-IILiga-IILigaNordReserve","BFV-IILiga-IILigaMitteReserve","BFV-IILiga-IILigaSuedReserve",
          "BFV-1Klassen-1KlasseNord/Spielplan","BFV-1Klasse-1Mitte","BFV-1Klassen-1KlasseSuedB",
            "BFV-1KL-1KlasseNordReserve","BFV-1KL-1KlasseMitteReserve","BFV-1KL-1KlasseSuedReserve"
          "BFV-2KL-2N","BFV-2Klassen-2KlasseMitte","BFV-2Klasse-2KlasseSuedA","BFV-2Klasse-2KlasseSuedB","BFV-2KL-2KlasseSuedC",
            "BFV-2KL-2KlasseNordReserve","BFV-2KL-2KlasseSuedAReserve","BFV-2KL-2KlasseSuedBReserve","BFV-2KL-2KlasseMitteReserve""BFV-2KL-2KlasseSuedCReserve"
          ]
    matches=set()
    # Match finder Thread:
    # Find matches to scrape and write to database

    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    #driverversion = driver.capabilities['moz:geckodriverVersion']
    #browserversion = driver.capabilities['browserVersion']


    # Match data scraper Thread
    # Scrape Data from Matches and save to Database
    years=["2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"]
    for year in years:
        for league in leagues:
            try:
                driver = webdriver.Firefox(options=options)
                matches.update(MatchFinder(driver,base_url.format(league,year)).getMatches())
                driver.close()
                for url in matches:
                    try:
                        driver = webdriver.Firefox(options=options)
                        to_database(MatchScraper(driver, url).get_data())
                        driver.close()
                    except:
                        print(traceback.format_exc())
                print("Successfully found {} matches".format(len(matches)))
            except:
                print(traceback.format_exc())

    print("DONE")