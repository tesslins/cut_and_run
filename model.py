import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, Float, String, Unicode
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
# from Maggie
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.engine.url import URL
# import sqlite3

engine = create_engine("postgresql+psycopg2://tessb@localhost:5432/routebase2",
                       echo=True)

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
    distance = Column(Float)
    ascent = Column(Float)
    descent = Column(Float)
    min_elevation = Column(Float)
    max_elevation = Column(Float)
    city = Column(Unicode)
    state = Column(Unicode)
    route_points_geojson = Column(String)
    start_lat = Column(Integer)
    start_lng = Column(Integer)
    end_lat = Column(Integer)
    end_lng = Column(Integer)
    
    def __init__(self, route_id, search_lat, search_lng, name, distance,
                 ascent, descent, min_elevation, max_elevation, city,
                 state, route_points_geojson, start_lat, start_lng, end_lat,
                 end_lng):
        self.route_id = route_id
        self.search_lat = search_lat
        self.search_lng = search_lng
        self.name = name
        self.distance = distance
        self.ascent = ascent
        self.descent = descent
        self.min_elevation = min_elevation
        self.max_elevation = max_elevation
        self.city = city
        self.state = state
        self.route_points_geojson = route_points_geojson
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        

def create_tables():
    Base.metadata.create_all(engine)
    
def main():
    pass

if __name__ == "__main__":
    main()
    


    