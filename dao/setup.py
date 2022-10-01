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
    match_id = Column(ForeignKey('matches.id'))
    team_id = Column(ForeignKey('teams.id'))


    player = relationship("Player", back_populates="matches", foreign_keys="[MatchPlayer.player_id]")
    match = relationship("Match", back_populates="players")
    team = relationship("Team", back_populates="players", foreign_keys="[MatchPlayer.team_id]",lazy='subquery')

    position = Column(String, nullable=True)
    goals = Column(Integer, nullable=True)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    starting_minute = Column(Integer, nullable=True)
    #substitution_minute = Column(Integer, nullable=True)
    #substitution_player= Column(Integer, ForeignKey('players.id'),nullable=True)

class Trainer(Base):
    __tablename__ = "trainers"
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)

    #home_matches = relationship('Match',  back_populates='trainers', foreign_keys="[Match.home_team_trainer_id]")
    #away_matches = relationship('Match', back_populates='trainers', foreign_keys="[Match.away_team_trainer_id]")

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
    away_team_trainer_id = Column(ForeignKey('trainers.id'))
    away_team_trainer = relationship("Trainer",  foreign_keys="[Match.away_team_trainer_id]")

    home_team_id = Column(ForeignKey('teams.id'))
    home_team = relationship("Team",  foreign_keys="[Match.home_team_id]",back_populates='home_matches')
    home_team_trainer_id = Column(ForeignKey('trainers.id'))
    home_team_trainer = relationship("Trainer",  foreign_keys="[Match.home_team_trainer_id]")

    players = relationship('MatchPlayer')  # ,lazy='subquery')
    activities = relationship('MatchActivity')

class Team(Base):
   __tablename__ = "teams"
   id = Column(Integer, primary_key=True)
   name = Column(String)
   year = Column(Integer)

   away_matches = relationship('Match',  primaryjoin="Match.away_team_id==Team.id")
   home_matches = relationship('Match',  primaryjoin="Match.home_team_id==Team.id")

   players = relationship('MatchPlayer')#,lazy='subquery')


class MatchActivity(Base):
   __tablename__ = "matches_activity"
   id = Column(Integer, primary_key=True)

   player_id = Column(Integer, ForeignKey('players.id'))
   substitution_player_id=Column(Integer, ForeignKey('players.id'))

   team_id = Column(Integer, ForeignKey('teams.id'))


   match_id = Column(ForeignKey('matches.id'))

   player = relationship("Player", foreign_keys="[MatchActivity.player_id]")
   team = relationship("Team", foreign_keys="[MatchActivity.team_id]")
   minute = Column(Integer, nullable=True)
   standing = Column(String, nullable=True)
   type = Column(String, nullable=True)
   text = Column(String, nullable=True)
   substitution_player = relationship("Player", foreign_keys="[MatchActivity.substitution_player_id]")


# Create the tables in the database
Base.metadata.create_all(engine)
