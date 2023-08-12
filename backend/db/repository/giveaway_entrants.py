from sqlalchemy.orm import Session
from schemas.giveaway_entrants import EntrantCreate
from db.models.giveaway_entrants import Lmp_Entrant as Entrant
from datetime import date


def create_new_entrant(
        entrant:EntrantCreate,
        db:Session):
    entrant = Entrant(
        email=entrant.email,
        zip_code=entrant.zip_code, 
        date_posted=date.today(),
        agree_tos=True,
    )
    try:
        db.add(entrant)
    except:
        print('\nDb Entrant addition failed\n')
        db.rollback()
    else:
        db.commit()
        db.refresh(entrant)
    finally:
        return entrant

    
def remove_entrant(
        entrant_email: str,
        db:Session):
    entrant = db.query(
        Entrant
    ).filter(Entrant.email == entrant_email).first()

    if entrant:
        db.delete(entrant)
        db.commit()
        return {"email": entrant_email}

