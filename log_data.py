from models import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
from passlib.context import CryptContext
#instantiate my cryptcontext
my_crypto_ctx = CryptContext(schemes=["sha256_crypt"])#"sha256_crypt","md5_crypt", "des_crypt"
#Insert data to the tables
Session=sessionmaker(bind=engine)
session=Session()
owner=Owner()
owner.email="kezziahbuyanzi@gmail.com"
owner.owner_name="Kezziah Buyanzi"
owner.status=2
owner.passcode=str(my_crypto_ctx.hash("123A"))
owner.dashpass=str(my_crypto_ctx.hash("kezzy2020!"))
owner.phone="254725154144"
#log ownerships table
ownership=Ownership()
ownership.ownership_id=1
ownership.card_uid="6b35fc0d"
ownership.email="kezziahbuyanzi@gmail.com"
ownership.start_date=dt.now()
ownership.doors=2
#log cards table
card=Card()
card.card_uid="6b35fc0d"
card.active=1
card.lost=0
#add the data, commit and close session
session.add(card)
session.add(owner)
session.add(ownership)
session.commit()
session.close()
