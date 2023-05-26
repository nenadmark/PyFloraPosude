from models.models import TemperatureReading, HumidityReading, PressureReading
from models.crud_inventory import get_plant_list

def create_temperature_reading(session, value):
    new_p_code = get_plant_list()
    new_temperature_reading = TemperatureReading(value=value, pot_id=new_p_code)
    session.add(new_temperature_reading)
    session.commit()

def create_humidity_reading(session, value):
    new_p_code = get_plant_list()
    new_humidity_reading = HumidityReading(value=value, pot_id=new_p_code)
    session.add(new_humidity_reading)
    session.commit()

def create_pressure_reading(session, value):
    new_p_code = get_plant_list()
    new_pressure_reading = PressureReading(value=value, pot_id=new_p_code)
    session.add(new_pressure_reading)
    session.commit()