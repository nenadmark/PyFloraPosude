from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models_1 import Base, Plants, Pots

engine = create_engine("sqlite:///inventory.db", echo=True)
Base.metadata.create_all(engine, checkfirst=True) 
Session = sessionmaker(bind=engine)
session = Session()

def get_data_plants():
    data_plants = session.query(Plants).all()
    return data_plants

def get_data_pots():
    data_plants = session.query(Pots).all()
    return data_plants


