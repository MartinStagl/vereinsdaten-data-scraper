from scraper.selenium_match_scraper import *
from scraper.selenium_match_finder import *
import pickle
from selenium import webdriver
import traceback
from dao.setup import *
import dao.database_connector as dbc
import sys
import utils.logger as lg
from datetime import datetime

def to_database(data):
    m = dbc.get_or_insert_match(data["url"])
    m.date = datetime.strptime(data["date"], "%d.%m.%Y")
    m.starttime = data["starttime"]
    m.league = data["league"]
    m.verband = data["verband"]
    m.round = data["round"]
    m.result = data["result"]

    home_team=dbc.get_or_insert_team(data["home_team_name"])
    away_team=dbc.get_or_insert_team(data["away_team_name"])
    
    home_team_trainer = dbc.get_or_insert_trainer(data["home_team_trainer"])
    away_team_trainer = dbc.get_or_insert_trainer(data["away_team_trainer"])

    m.home_team_trainer=home_team_trainer
    m.away_team_trainer=away_team_trainer
    #dbc.insert_teams(home_team,away_team)

    for player in data["home_players"]:
        p = dbc.get_or_insert_player(player["url"])
        p.name= player["name"]
        #p.birthyear=player["birthyear"]
        #p.nationality = player["nationality"]
        mp=dbc.get_or_insert_match_player(match_id=m.id,player_id=p.id,team_id=home_team.id)
        mp.player=p
        mp.goals=player["goals"]
        mp.position = player["position"]
        mp.red_cards = player["red_cards"]
        mp.yellow_cards = player["yellow_cards"]
        mp.team=home_team
        mp.match=m
        #mp.starting_minute = player["starting_minute"]
        #mp.substitution_player = player["substitution_player"]
        #mp.substitution_minute = player["substitution_minute"]
        #home_team.players.append(p)
        home_team.players.append(mp)
        dbc.insert_player(p)


        #home_team.players.append(player)

    for player in data["away_players"]:
        p = dbc.get_or_insert_player(player["url"])
        p.name= player["name"]
        #p.birthyear=player["birthyear"]
        #p.nationality = player["nationality"]
        mp=dbc.get_or_insert_match_player(match_id=m.id,player_id=p.id,team_id=away_team.id)
        mp.player=p
        mp.goals=player["goals"]
        mp.position = player["position"]
        mp.red_cards = player["red_cards"]
        mp.yellow_cards = player["yellow_cards"]
        mp.team = away_team
        mp.match = m
        #mp.starting_minute = player["starting_minute"]
        #mp.substitution_player = player["substitution_player"]
        #mp.substitution_minute = player["substitution_minute"]
        away_team.players.append(mp)
        dbc.insert_player(p)
        #m.players.append(mp)

    for activity in data["activities"]:
        a=MatchActivity()
        a.text=activity["text"]
        if activity["team"]=="home":
            a.team=home_team
        else:
            a.team=away_team
        a.player=dbc.get_or_insert_player(activity["player"])
        a.minute=activity["minute"]
        a.standing=activity["standing"]
        if activity["substitution_player"]!="":
            a.substitution_player=dbc.get_or_insert_player(activity["substitution_player"])
        a.type=activity["type"]
        m.activities.append(a)

    m.away_team = away_team
    m.home_team = home_team

    dbc.insert_match(m)
    dbc.session.close()


if __name__ == "__main__":

    log=lg.initLogger()

    #start_url="https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/BFV-2KL-2N/Spielplan/aktuell/{}"
    base_url="https://www.oefb.at/bewerbe/Spiel/Aufstellung/{}"
    leagues = [   "BFV-NeuerEintrag-RegionalligaOst","BFV-Regionalliga-RegionalligaOst",
        "BFV-BVZBurgenlandliga-BVZBurgenlandliga","BFV-BL-BurgenlandligaReserve",
        "BFV-Burgenlandliga-BurgenlandligaReserve",
        "BFV-IILigen-IILigaNord", "BFV-IILiga-IILigaMitte", "BFV-IILigen-IILigaSued",
        "BFV-IILiga-IILigaNordReserve", "BFV-IILiga-IILigaMitteReserve", "BFV-IILiga-IILigaSuedReserve",
        "BFV-1Klassen-1KlasseNord/Spielplan", "BFV-1Klasse-1Mitte", "BFV-1Klassen-1KlasseSuedB",
        "BFV-1KL-1KlasseNordReserve", "BFV-1KL-1KlasseMitteReserve", "BFV-1KL-1KlasseSuedReserve",
        "BFV-2KL-2N", "BFV-2Klassen-2KlasseMitte", "BFV-2Klasse-2KlasseSuedA", "BFV-2Klasse-2KlasseSuedB",
        "BFV-2KL-2KlasseSuedC",
        "BFV-2KL-2KlasseNordReserve", "BFV-2KL-2KlasseSuedAReserve", "BFV-2KL-2KlasseSuedBReserve",
        "BFV-2KL-2KlasseMitteReserve", "BFV-2KL-2KlasseSuedCReserve"
    ]
    matches=set()


    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    #driverversion = driver.capabilities['moz:geckodriverVersion']
    #browserversion = driver.capabilities['browserVersion']


    # Match data scraper Thread
    # Scrape Data from Matches and save to Database
    years=["2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2022"]
    
    driver = webdriver.Firefox(options=options)
    league_urls=set()
    #for league in leagues:
    #    try:
    #        league_urls.update(MatchFinder(driver,url='https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/{}/Spielplan'.format(league)).getLeagueUrls())
    #    except:
    #        log.info(traceback.format_exc())
    #log.info("Fetches {} leagues from BFV".format(len(league_urls)))
    match_id=dbc.get_last_match()
    try:            
        for match_url_id in range(match_id,3200000):
            try:
                driver = webdriver.Firefox(options=options)
                #matches=set()
                #matches.update(MatchFinder(driver,base_url.format(league_url.replace("Tabelle","Spielplan"))).getMatches())
                #matches_in_db=dbc.get_matches()
                #temp_set=matches-matches_in_db
                #log.info(len(temp_set))
                #for url in temp_set:
                    
                #driver = webdriver.Firefox(options=options)
                url=base_url.format(match_url_id)
                data={}
                data=MatchScraper(driver, url).get_formation()
                data.update(MatchScraper(driver,url).get_activities())
                to_database(data)
                driver.close()
                driver.quit()
            except:
                log.info(traceback.format_exc())
    except:
        log.info(traceback.format_exc())
    log.info("DONE with scrapeing {}".format(len(dbc.get_matches())))
    driver.close()
