import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from tables.houses import House
from tables.emails import Email
from tables.attempts import Attempt

class DBQueries:
    
    def __init__(self, username: str, password: str, host: str, database: str) -> None:
        connection_str = f'postgresql://{username}:{password}@{host}:5432/{database}'
        engine = create_engine(connection_str)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def add_house_if_not_exists(self, house: House) -> bool:
        exists = self.session.query(House).filter_by(link=house.link).first() is not None
        if not exists:
            self.session.add(house)
            self.session.commit()
            return True
        return False 
    
    def add_email(self, email: Email) -> None:
        self.session.add(email)
        self.session.commit()
        
    def add_attempt(self, attempt: Attempt) -> None:
        self.session.add(attempt)
        self.session.commit()
        
    def get_last_email_timestamp(self) -> datetime:
        last_email_timestamp = self.session.query(func.max(Email.timestamp)).first()[0]
        if last_email_timestamp is None:
            return datetime(1970, 1, 1)
        return last_email_timestamp
    
    def get_houses_after_timestamp(self, timestamp: datetime) -> list[House]:
        houses_after_timestamp = self.session.query(House).where(House.timestamp > timestamp).all()
        return houses_after_timestamp