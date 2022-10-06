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

def get_or_insert_trainer(name):
    trainer = session.query(Trainer).filter_by(name=name).first()
    if not trainer:
        trainer = Trainer()
        trainer.name = name
    return trainer

def get_or_insert_team(name):
    team = session.query(Team).filter_by(name=name).first()
    if not team:
        team = Team()
        team.name=name
    return team

def get_or_insert_match(url):
    match = session.query(Match).filter_by(url=url).first()
    if not match:
        match = Match()
        match.url = url
    return match

def get_matches():
    matches = session.query(Match.url)
    return set(matches)