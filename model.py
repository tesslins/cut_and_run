import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
# http://sqlalchemy-utils.readthedocs.org/en/latest/_modules/sqlalchemy_utils/types/json.html
from sqlalchemy.dialects.postgresql import JSON

# http://docs.sqlalchemy.org/en/latest/core/engines.html#postgresql
engine = create_engine("postgresql+psycopg2://tess:2kittens@localhost:5001/routedb",
                       use_native_hstore=False)
# ?? need to add: echo = False or convert_unicode=True ??
session = scoped_session(sessionmaker(bind=engine,
                                       autocommit = False,
                                       autoflush = False))
Base = declarative_base()
Base.query = session.query_property()
    

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key = True)
    route_id = Column(String(10), nullable = False)
    route_object = Column(JSON, nullable = False)
    route_geojson = Column(JSON, nullable = False)
    # start_latlng
    # end_latlng
    # distance
    
    def __init__(self, route_id, route_object, route_geojson):
        self.route_id = route_id
        self.route_object = route_object
        self.route_geojson = route_geojson

class RouteObject(Base):
    __tablename__ = "route_objects"
    id = Column(Integer, primary_key = True)
    lat_lng = Column(String(50), nullable=False)
    #min_distance = Column(Integer, nullable = False)
    #max_distance = Column(Integer, nullable = False)
    #routes_object = Column(JSON, nullable = False)
    
    def __init__(self, lat_lng):
        self.lat_lng = lat_lng
        #self.min_distance = min_distance
        #self.max_distance = max_distance
        #self.routes_object = routes_object
    


    