from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models.models import Base, Plant, Pot
import random

engine_inventory = create_engine("sqlite:///PyFloraDB.db", echo=True)
Base.metadata.create_all(engine_inventory, checkfirst=True) 
Session = sessionmaker(bind=engine_inventory)
session = Session()

def get_plant_list():
    p_codes = [plants.id for plants in session.query(Plant).all()]
    random_p_code = random.choice(p_codes)
    return random_p_code

def get_data_plants():
    data_plants = session.query(Plant).all()
    return data_plants

def get_data_pots():
    data_pots = session.query(Pot).options(joinedload(Pot.plant)).all()
    return data_pots

def delete_plant(id):
    del_plant = session.query(Plant).get(id)
    if del_plant:
        session.delete(del_plant)
        session.commit()

def delete_pot(id):
    del_pot = session.query(Pot).get(id)
    if del_pot:
        session.delete(del_pot)
        session.commit()

def create_plant(name, sort, humidity, temperature, p_code, image_path):
    new_plant = Plant(
        name=name,
        sort=sort,
        humidity=humidity,
        temperature=temperature,
        p_code=p_code,
        image_path=image_path
    )
    session.add(new_plant)
    session.commit()

def create_pot(name, radius, image_path):
    new_pot = Pot(
        name=name,
        radius=radius,
        image_path=image_path
    )
    session.add(new_pot)
    session.commit()

def update_plant(id, name=None, sort=None, humidity=None, temperature=None, p_code=None, image_path=None):
    plant = session.query(Plant).get(id)
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
    pot = session.query(Pot).get(id)
    if pot:
        if name is not None:
            pot.name = name
        if radius is not None:
            pot.radius = radius
        if image_path is not None:
            pot.image_path = image_path
        session.commit()