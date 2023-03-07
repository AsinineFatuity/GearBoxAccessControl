from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from datetime import datetime

import json

from models import Ownership,Owner

engine=create_engine("mysql+pymysql://asinine:a69ine2020!@127.0.0.1:3306/access_control")
Session=sessionmaker(bind=engine)
session=Session()

authenticate_topic="acc/auth"

def topic_data_handler(topic,jsondata):
    my_data_Dict=json.loads(jsondata)
    if topic=="acc/s/rfid":
        rfid=my_data_Dict["rfid"]
        door=int(my_data_Dict["door"])
        authenticate_user_with_rfid(rfid,door)
    if topic=="acc/s/pin":
        pin=my_data_Dict["pin"]
        phone=my_data_Dict["phone"]
        door=int(my_data_Dict["door"])
        authenticate_user_with_pin(pin,phone,door)
    if topic=="acc/s/master":
        #write the code to extract the rfids that are scanned by the master.
        pass
def fail_success_pub(flag,door_accessed):
    from paho_mqtt_listen import publish
    if flag==True:
        success_msg=str(door_accessed)+str(1)
        publish(authenticate_topic,success_msg)
    if flag==False:
        fail_msg=str(door_accessed)+str(0)
        publish(authenticate_topic,fail_msg)
#do my database queries here
ownerships=session.query(Ownership).all()
owners=session.query(Owner).all()
#then write the functions to authenticate the user with the different credentials

def authenticate_user_with_rfid(rfid,door):
    for ownership in ownerships:
        if ownership.card_uid==rfid:
            if ownership.end_date is None or ownership.end_date>datetime.now():
                if (ownership.doors>>(door-1))&1:
                    fail_success_pub(True,door)
                else: fail_success_pub(False,door)                         
            else: fail_success_pub(False,door)                  
        else: fail_success_pub(False,door)       
                    
def authenticate_user_with_pin(pin,phone,door):
    for owner in owners:
        if owner.phone==phone:
            for ownership in ownerships:
                if ownership.end_date is None or ownership.end_date>datetime.now():
                    if owner.passcode==pin:
                        if (ownership.doors>>(door-1))&1:
                            fail_success_pub(True,door)
                        else: fail_success_pub(False,door)               
                    else:  fail_success_pub(False,door)              
                else: fail_success_pub(False,door)                  
        else: fail_success_pub(False,door)
            
session.close()
