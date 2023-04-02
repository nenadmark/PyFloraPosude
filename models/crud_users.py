from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User

engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(engine, checkfirst=True) 
Session = sessionmaker(bind=engine)
session = Session()

def login_user(login_email, login_password):
    return session.query(User).filter_by(
        email=login_email, 
        password=login_password
    ).first()