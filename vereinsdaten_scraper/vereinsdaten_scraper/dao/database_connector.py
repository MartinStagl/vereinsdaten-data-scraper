from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from .setup import *

engine = create_engine('sqlite:///verbands.db', echo=True)
conn = engine.connect()


def insert(p:Player,m:Match,home_team:Team,away_team:Team):
    with Session(bind=engine) as session:
        # add users
        session.add(p)
        session.commit()
        session.add(home_team)
        session.commit()
        session.add(away_team)
        session.commit()
        session.add(m)
        session.commit()