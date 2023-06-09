import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models.models import Base, Plant, Pot, TemperatureReading, HumidityReading

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

def create_plant(name, sort, ref_temperature, ref_humidity, ref_salinity, p_code, image_path):
    new_plant = Plant(
        name=name,
        sort=sort,
        ref_temperature=ref_temperature,
        ref_humidity=ref_humidity,
        ref_salinity=ref_salinity,
        p_code=p_code,
        image_path=image_path
    )
    session.add(new_plant)
    session.commit()

def create_pot(name, radius, humidity, temperature, image_path):
    new_pot = Pot(
        name=name,
        radius=radius,
        humidity=humidity,
        temperature=temperature,
        image_path=image_path
    )
    session.add(new_pot)
    session.commit()

def update_plant(id, name=None, sort=None, ref_temperature=None, ref_humidity=None, ref_salinity=None, p_code=None, image_path=None):
    plant = session.query(Plant).get(id)
    if plant:
        if name is not None:
            plant.name = name
        if sort is not None:
            plant.sort = sort
        if ref_temperature is not None:
            plant.ref_temperature = ref_temperature
        if ref_humidity is not None:
            plant.ref_humidity = ref_humidity
        if ref_salinity is not None:
            plant.ref_salinity = ref_salinity
        if p_code is not None:
            plant.p_code = p_code
        if image_path is not None:
            plant.image_path = image_path
        session.commit()

def update_pot(id, name=None, radius=None, humidity=None, temperature=None, image_path=None):
    pot = session.query(Pot).get(id)
    if pot:
        if name is not None:
            pot.name = name
        if radius is not None:
            pot.radius = radius
        if humidity is not None:
            pot.humidity = humidity
        if temperature is not None:
            pot.temperature = temperature
        if image_path is not None:
            pot.image_path = image_path
        session.commit()

def get_temperature_readings(pot_id):
    return session.query(TemperatureReading).filter(TemperatureReading.pot_id == pot_id).all()

def get_humidity_readings(pot_id):
    return session.query(HumidityReading).filter(HumidityReading.pot_id == pot_id).all()
