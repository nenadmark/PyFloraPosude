from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import InventoryBase, Plants, Pots
import random

engine_inventory = create_engine("sqlite:///inventory.db", echo=True)
InventoryBase.metadata.create_all(engine_inventory, checkfirst=True) 
Session = sessionmaker(bind=engine_inventory)
session = Session()

def get_plant_list():
    p_codes = [plants.p_code for plants in session.query(Plants).all()]
    random_p_code = random.choice(p_codes)
    return random_p_code

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

def update_plant(id, name=None, sort=None, humidity=None, temperature=None, p_code=None, image_path=None):
    plant = session.query(Plants).get(id)
    if plant:
        if name is not None:
            plant.name = name
        if sort is not None:
            plant.sort = sort
        if humidity is not None:
            plant.humidity = humidity
        if temperature is not None:
            plant.temperature = temperature
        if p_code is not None:
            plant.p_code = p_code
        if image_path is not None:
            plant.image_path = image_path
        session.commit()

def update_pot(id, name=None, radius=None, image_path=None):
    pot = session.query(Pots).get(id)
    if pot:
        if name is not None:
            pot.name = name
        if radius is not None:
            pot.radius = radius
        if image_path is not None:
            pot.image_path = image_path
        session.commit()