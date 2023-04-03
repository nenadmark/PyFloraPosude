from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import InventoryBase, Plants, Pots

engine_inventory = create_engine("sqlite:///inventory.db", echo=True)
InventoryBase.metadata.create_all(engine_inventory, checkfirst=True) 
Session = sessionmaker(bind=engine_inventory)
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