"""Create database connection"""
from sqlalchemy import create_engine, engine,Column,Integer,String,DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy_utils import  EmailType #PasswordType,

#Instantiate the declarative base class to process the instrumentation
Base = declarative_base()
#Initialize database parameters
host = "127.0.0.1"         
user = "asinine"          
password = "a69ine2020!"    
db_name = "access_control"
port=3306

engine=create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}",
    echo=True,
)

#Create the owners' table to store the data of RFID Card Owners
class Owner(Base):
    __tablename__='owners'
    email=Column(EmailType,primary_key=True)
    owner_name=Column(String(32))
    status=Column(Integer)
    passcode=Column(String(128))
    dashpass=Column(String(128))
    phone=Column(String(12),unique=True)
    confirmed=Column(Boolean,default=0)
    owners_ownership=relationship("Ownership")
#Create the Cards table 
class Card(Base):
    __tablename__='cards' 
    card_uid=Column(String(8),primary_key=True)
    active=Column(Boolean)
    lost=Column(Boolean)
    cards_ownership=relationship("Ownership")
    cards_breached=relationship("Breach")

#Create the Ownership table so as to micromanage owners using their RFID
class Ownership(Base):
    __tablename__='ownerships'
    ownership_id=Column(Integer,primary_key=True,autoincrement=True)
    card_uid=Column(String(32),ForeignKey("cards.card_uid"))
    email=Column(EmailType,ForeignKey("owners.email"))
    ownership_logs=relationship("Log")
    start_date=Column(DateTime)
    end_date=Column(DateTime,nullable=True)
    doors=Column(Integer)
#Create a table for the doors
class Door(Base):
    __tablename__='doors'
    door_id=Column(Integer,primary_key=True,autoincrement=True)
    door_name=Column(String(45))
    doors_breached=relationship("Breach")
    doors_logged=relationship("Log")
#Create my logs table to store and display the log data
class Log(Base):
    __tablename__='logs'
    log_id=Column(Integer,primary_key=True,autoincrement=True)
    ownership_id=Column(Integer,ForeignKey("ownerships.ownership_id"))
    door_id=Column(Integer,ForeignKey("doors.door_id"))
    date=Column(DateTime)
#Create a table to handle the breaches involved
class Breach(Base):
    __tablename__='breaches'
    breach_id=Column(Integer,primary_key=True,autoincrement=True)
    card_uid=Column(String(8))
    datetime=Column(DateTime)
    door_id=Column(Integer,ForeignKey("doors.door_id"))
    card_uid=Column(String(32),ForeignKey("cards.card_uid"))
#Run the Code to create all the tables
Base.metadata.create_all(bind=engine)
