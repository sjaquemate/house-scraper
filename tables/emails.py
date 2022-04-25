from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'
    address = Column(Text, primary_key=True)
    timestamp = Column(TIMESTAMP)
    
    def __repr__(self):
        return str(self.__dict__)