from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Attempt(Base):
    __tablename__ = 'attempts'
    timestamp = Column(TIMESTAMP, primary_key=True)
    total_houses = Column(Integer)
    num_new_houses = Column(Integer)
    
    def __repr__(self):
        return str(self.__dict__)