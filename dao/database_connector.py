from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from .setup import *

engine = create_engine('sqlite:///verbands.db', echo=True)
conn = engine.connect()


session = Session(engine)


def insert_player(p:Player):
    print("Inserting new player")
    session.add(p)
    session.commit()
def insert_match(m:Match):
    # add users
    print("Inserting new match")
    session.commit()
    session.add(m)
    session.commit()

def insert_teams(home_team:Team,away_team:Team):
    # add users
    print("Inserting new teams")
    session.add(home_team)
    session.commit()
    session.add(away_team)
    session.commit()
def get_or_insert_player(url):
    player = session.query(Player).filter_by(url=url).first()
    if not player:
        player = Player()
        player.url=url
    return player


def get_or_insert_team(name):
    team = session.query(Team).filter_by(name=name).first()
    if not team:
        team = Team()
        team.name=name
    return team