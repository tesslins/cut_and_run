import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, Float, String, Unicode
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///routebase.db", echo = True)

session = scoped_session(sessionmaker(bind=engine,
                                       autocommit = False,
                                       autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key = True)
    route_id = Column(Integer)
    search_lat = Column(Unicode)
    search_lng = Column(Unicode)
    name = Column(Unicode)
    description = Column(Unicode)
    distance = Column(Float)
    ascent = Column(Float)
    descent = Column(Float)
    min_elevation = Column(Float)
    max_elevation = Column(Float)
    city = Column(Unicode)
    state = Column(Unicode)

def main():
    pass

if __name__ == "__main__":
    main()
    


    