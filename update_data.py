from models import *
from sqlalchemy.orm import sessionmaker
import datetime
from passlib.context import CryptContext
#instantiate my cryptcontext
my_crypto_ctx = CryptContext(schemes=["sha256_crypt"])
Session=sessionmaker(bind=engine)
session=Session()

# ownership=session.query(Ownership).filter(Ownership.ownership_id==1).first()
# ownership.doors=1
owner=session.query(Owner).filter(Ownership.ownership_id==1).first()
owner.passcode=str(my_crypto_ctx.hash("123A"))
owner.phone="25400000"
# ownership.end_date=ownership.start_date+datetime.timedelta(days=3)

session.commit()
session.close()
#old users
# owner.email="asininefatuity@gmail.com"
# owner.name="Asinine Fatuity"
# owner.owner_status=2
# owner.passcode=str(my_crypto_ctx.hash("1234"))
# owner.dashpass=str(my_crypto_ctx.hash("asinine2020!"))
# owner.phone="254711653675"
# #log ownerships table
# ownership=Ownership()
# ownership.id=1
# ownership.card_id="F7DAA633"
# ownership.owners_id="asininefatuity@gmail.com"
# ownership.start_date=dt.now()
# ownership.doors=2
# #log cards table
# card=Card()
# card.card_id="F7DAA633"
# card.card_status=True