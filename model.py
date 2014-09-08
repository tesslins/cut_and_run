import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, Float, String, Unicode, Numeric
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from geoalchemy2.types import Geometry


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
    route_id = Column(Numeric)
    name = Column(Unicode)
    distance = Column(Numeric)
    ascent = Column(Numeric)
    descent = Column(Numeric)
    min_elevation = Column(Numeric)
    max_elevation = Column(Numeric)
    city = Column(Unicode)
    state = Column(Unicode)
    start_lng = Column(Numeric)
    start_lat = Column(Numeric)
    end_lng = Column(Numeric)
    end_lat = Column(Numeric)
    start_point = Column(Geometry(geometry_type='POINT', srid=4326))
    end_point = Column(Geometry(geometry_type='POINT', srid=4326))
    route_points_geojson = Column(String)
    
    def __init__(self, route_id, name, distance, ascent, descent, min_elevation,
                 max_elevation, city, state, start_lng, start_lat, end_lng,
                 end_lat, start_point, end_point, route_points_geojson):
        self.route_id = route_id
        self.name = name
        self.distance = distance
        self.ascent = ascent
        self.descent = descent
        self.min_elevation = min_elevation
        self.max_elevation = max_elevation
        self.city = city
        self.state = state
        self.start_lng = start_lng
        self.start_lat = start_lat
        self.end_lng = end_lng
        self.end_lat = end_lat
        self.start_point = start_point
        self.end_point = end_point
        self.route_points_geojson = route_points_geojson
        
def create_tables():
    Base.metadata.create_all(engine)
    
def main():
    pass

if __name__ == "__main__":
    main()
    


    