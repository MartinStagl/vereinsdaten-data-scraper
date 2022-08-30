from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from .setup import *

engine = create_engine('sqlite:///verbands.db', echo=True)
conn = engine.connect()

def insert_player(p:Player):
    with Session(bind=engine) as session:
        print("Inserting new player")
        session.add(p)
        session.commit()
def insert(m:Match,home_team:Team,away_team:Team):
    with Session(bind=engine) as session:
        # add users
        print("Inserting new match")
        session.add(home_team)
        session.commit()
        session.add(away_team)
        session.commit()
        session.add(m)
        session.commit()


def get_or_insert_player(url):
    with Session(bind=engine) as session:
        player = session.query(Player).filter_by(url=url).first()
        if not player:
            player = Player()
            player.url=url
        return player


def get_or_insert_team(name):
    with Session(bind=engine) as session:
        team = session.query(Team).filter_by(name=name).first()
        if not team:
            team = Team()
            team.name=name
        session.add(team)
        session.commit()
    return team