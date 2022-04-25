from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class House(Base):
    __tablename__ = 'houses'
    link = Column(Text, primary_key=True)
    name = Column(Text)
    timestamp = Column(TIMESTAMP)
    makelaar = Column(Text)
    price = Column(Text)
    
    def __repr__(self):
        return str(self.__dict__)