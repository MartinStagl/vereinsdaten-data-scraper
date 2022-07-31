from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from setup import *

engine = create_engine('sqlite:///verbands.db', echo=True)
conn = engine.connect()


def insert(players: list):
   # Test it
   for player in players:
      with Session(bind=engine) as session:

          # add users
          usr1 = Player(name="bob")
          session.add(usr1)

          usr2 = Player(name="alice")
          session.add(usr2)

          session.commit()

          # add projects
          prj1 = Team(name="Project 1")
          session.add(prj1)

          prj2 = Team(name="Project 2")
          session.add(prj2)

          session.commit()

          # map users to projects
          prj1.players = [usr1, usr2]
          prj2.players = [usr2]

          session.commit()