from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine('postgresql://tess:2kittens@localhost/test')

Base = declarative_base()
        
        
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
    


    