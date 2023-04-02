from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, Plants, Pots

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

def delete_plant(id):
    del_plant = session.query(Plants).get(id)
    if del_plant:
        session.delete(del_plant)
        session.commit()

def delete_pot(id):
    del_pot = session.query(Pots).get(id)
    if del_pot:
        session.delete(del_pot)
        session.commit()