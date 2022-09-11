from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean, Date
from sqlalchemy.orm import declarative_base, relationship, Session


# https://docs.sqlalchemy.org/en/14/orm/dataclasses.html#mapping-dataclasses-using-declarative-with-imperative-table


# Make the engine
#engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)
engine = create_engine('sqlite:///verbands.db', echo=True)
# Make the DeclarativeMeta
Base = declarative_base()


class MatchPlayer(Base):
    __tablename__ = "matches_players"
    id = Column(Integer, primary_key=True)

    player_id = Column(ForeignKey('players.id'))
    #match_id = Column(ForeignKey('matches.id'))
    team_id = Column(ForeignKey('teams.id'))


    player = relationship("Player", back_populates="matches", foreign_keys="[MatchPlayer.player_id]")
    #match = relationship("Match", back_populates="players")
    team = relationship("Team", back_populates="players", foreign_keys="[MatchPlayer.team_id]",lazy='subquery')

    position = Column(String, nullable=True)
    goals = Column(Integer, nullable=True)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    starting_minute = Column(Integer, nullable=True)
    substitution_minute = Column(Integer, nullable=True)
    substitution_player= Column(Integer, ForeignKey('players.id'),nullable=True)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    url = Column(String,unique=True)
    name = Column(String)
    nationality=Column(String)
    birthyear=Column(Integer)
    matches = relationship('MatchPlayer',  back_populates='player', foreign_keys="[MatchPlayer.player_id]")
    #teams = relationship('Team', secondary='teams_players',  back_populates='players')

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    url = Column(String,nullable=True,unique=True)
    date= Column(Date,nullable=True)
    starttime= Column(String,nullable=True)
    league=Column(String,nullable=True)
    round = Column(Integer,nullable=True)
    result= Column(Integer,nullable=True)

    away_team_id=Column(ForeignKey('teams.id'))
    away_team = relationship("Team",  foreign_keys="[Match.away_team_id]",back_populates='away_matches')

    home_team_id = Column(ForeignKey('teams.id'))
    home_team = relationship("Team",  foreign_keys="[Match.home_team_id]",back_populates='home_matches')

    #players = relationship('MatchPlayer', back_populates='match')

class Team(Base):
   __tablename__ = "teams"
   id = Column(Integer, primary_key=True)
   name = Column(String)
   year = Column(Integer)

   away_matches = relationship('Match',  primaryjoin="Match.away_team_id==Team.id")
   home_matches = relationship('Match',  primaryjoin="Match.home_team_id==Team.id")

   players = relationship('MatchPlayer')#,lazy='subquery')


class TeamPlayer(Base):
   __tablename__ = "teams_players"
   id = Column(Integer, primary_key=True)
   player_id = Column(Integer, ForeignKey('players.id'))
   team_id = Column(Integer, ForeignKey('teams.id'))


# Create the tables in the database
Base.metadata.create_all(engine)
