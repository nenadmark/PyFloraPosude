import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, unique=False) 
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_admin= db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return self.name

#dodati doilje sve sta treba returnat


class Plants(Base):
    __tablename__= "plants"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sort = db.Column(db.String, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    p_code = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String)

    #def __repr__(self) -> str:
        #return self.id, self.name, self.sort, self.humidity, self.humidity, self.temperature, self.p_code, self.image_path
    
class Pots(Base):
    __tablename__= "pots"  

    id = db.Column(db.String, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    p_code = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=False)

    #def __repr__(self) -> str:
        #return self.name
    


"""
##new gpt shit

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

# Create user table
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT, is_admin BOOL)''')

# Create inventory table
c.execute('''CREATE TABLE inventory
             (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)''')

# Insert admin user
c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")

# Insert inventory items
c.execute("INSERT INTO inventory (name, quantity, price) VALUES ('Plant 1', 10, 19.99)")
c.execute("INSERT INTO inventory (name, quantity, price) VALUES ('Plant 2', 5, 29.99)")
c.execute("INSERT INTO inventory (name, quantity, price) VALUES ('Pot 1', 20, 9.99)")
c.execute("INSERT INTO inventory (name, quantity, price) VALUES ('Pot 2', 15, 14.99)")

conn.commit()
conn.close()"""