from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User

engine_users = create_engine("sqlite:///PyFloraDB.db", echo=True)
Base.metadata.create_all(engine_users, checkfirst=True) 
Session = sessionmaker(bind=engine_users)
session = Session()

def login_user(login_email, login_password):
    return session.query(User).filter_by(
        email=login_email, 
        password=login_password
    ).first()