
from setup import *

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///verbands.db.working', echo=True)

# Test it
with Session(bind=engine) as session:

    m = Match()
    session.add(m)

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


with Session(bind=engine) as session:

    print(*session.query(Player).where(Player.id == 1).one().teams)
    print(*session.query(Team).where(Team.id == 1).one().players)