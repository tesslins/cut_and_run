import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
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
    route_id = Column(String(10), nullable = False)
    route_geojson = Column(String, nullable = False)
    # start_latlng
    # end_latlng
    # distance

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
    


    