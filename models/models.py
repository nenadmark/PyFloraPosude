import sqlalchemy as db
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_admin= db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return self.name

class Plant(Base):
    __tablename__= "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sort = db.Column(db.String, nullable=False)
    p_code = db.Column(db.String, ForeignKey('pots.id'))
    image_path = db.Column(db.String, nullable=True)
    ref_temperature = db.Column(db.Integer, nullable=False, default=20)
    ref_humidity = db.Column(db.Integer, nullable=False, default=50)
    ref_salinity = db.Column(db.Float, nullable=False, default=1.8)
    pot = relationship("Pot", back_populates="plant")

class Pot(Base):
    __tablename__= "pots"  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    plant = relationship("Plant", back_populates="pot", uselist=False)
    humidity = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)

class TemperatureReading(Base):
    __tablename__ = "temperature_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)
    pot = db.Column(db.String)

class HumidityReading(Base):
    __tablename__ = "humidity_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)
    pot = db.Column(db.String)

class PressureReading(Base):
    __tablename__ = "pressure_readings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)
    pot = db.Column(db.String)