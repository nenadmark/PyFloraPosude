from models.models import TemperatureReading, HumidityReading, PressureReading

def create_temperature_reading(session, value):
    new_temperature_reading = TemperatureReading(value=value)
    session.add(new_temperature_reading)
    session.commit()

def create_humidity_reading(session, value):
    new_humidity_reading = HumidityReading(value=value)
    session.add(new_humidity_reading)
    session.commit()

def create_pressure_reading(session, value):
    new_pressure_reading = PressureReading(value=value)
    session.add(new_pressure_reading)
    session.commit()