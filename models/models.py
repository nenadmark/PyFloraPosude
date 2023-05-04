import sqlalchemy as db
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

UserBase = declarative_base()
InventoryBase = declarative_base()
MeteoBase = declarative_base()

class User(UserBase):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_admin= db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return self.name

class Plants(InventoryBase):
    __tablename__= "plants"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sort = db.Column(db.String, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    temperature = Column(Integer, nullable=False)
    p_code = Column(String, ForeignKey('pots.id'))
    image_path = db.Column(db.String)

    ref_temperature = db.Column(db.Integer, nullable=False, default=20)
    ref_humidity = db.Column(db.Integer, nullable=False, default=50)
    ref_salinity = db.Column(db.Integer, nullable=False, default=1.8)

    pot = relationship("Pots", back_populates="plants")

class Pots(InventoryBase):
    __tablename__= "pots"  

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String, nullable=False)

    plants = relationship("Plants", back_populates="pot")

class TemperatureReading(MeteoBase):
    __tablename__ = "temperature_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

class HumidityReading(MeteoBase):
    __tablename__ = "humidity_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

class PressureReading(MeteoBase):
    __tablename__ = "pressure_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)