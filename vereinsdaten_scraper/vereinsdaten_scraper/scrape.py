from scraper.selenium_match_scraper import *
from scraper.selenium_match_finder import *


from dao.setup import *
import dao.database_connector as dbc

def to_database(data):
    m = Match()
    m.url = data["url"]
    m.date = data["date"]
    m.starttime = data["starttime"]
    m.league = data["league"]
    m.round = data["round"]
    m.result = data["result"]

    home_team=Team()
    home_team.name=data["home_team_name"]
    away_team=Team()
    away_team.name = data["away_team_name"]
    for player in data["home_players"]:
        p = Player()
        p.name= player["name"]
        p.url = player["url"]
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
        m.players.append(mp)

        #home_team.players.append(player)

    for player in data["away_players"]:
        p = Player()
        p.name= player["name"]
        p.url = player["url"]
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
        m.players.append(mp)
        #away_team.players.append(player)

    m.away_team = away_team
    m.home_team = home_team

    dbc.insert(p,m,home_team,away_team)


if __name__ == "__main__":
    start_url="https://www.bfv.at/Portal/Spielbetrieb/Ergeb-Tabellen/BFV-2KL-2N/Spielplan/aktuell/2022"
    matches=set()
    # Match finder Thread:
    # Find matches to scrape and write to database
    matches.update(MatchFinder(start_url).getMatches())
    print("Successfully found {} matches".format(len(matches)))
    # Match data scraper Thread
    # Scrape Data from Matches and save to Database
    for url in matches:
        to_database(MatchScraper(url).get_data())
    print("DONE")