from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import declarative_base, relationship, Session

# Make the engine
#engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)
engine = create_engine('sqlite:///verbands.db', echo=True)
# Make the DeclarativeMeta
Base = declarative_base()


class Association(Base):
    __tablename__ = "association"
    left_id = Column(ForeignKey("left.id"), primary_key=True)
    right_id = Column(ForeignKey("right.id"), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")
    #brother= Column(ForeignKey("right.id"),nullable=True)


class Parent(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")


class Child(Base):
    __tablename__ = "right"
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child", foreign_keys="[Association.right_id]" )



# Create the tables in the database
Base.metadata.create_all(engine)

# Test it
with Session(bind=engine) as session:

    # create parent, append a child via association
    p = Parent()
    session.add(p)
    a = Association(extra_data="some data")
    a.child = Child()
    session.add(a)
    p.children.append(a)
    session.add(p)

    session.add(p)


    # iterate through child objects via association, including association
    # attributes
    for assoc in p.children:
        print(assoc.extra_data)
        print(assoc.child)


    session.commit()


with Session(bind=engine) as session:

    print(session.query(Parent).where(Parent.id == 1).one().children)