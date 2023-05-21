from sqlalchemy.orm import Session
from schemas.giveaway_entrants import EntrantCreate
from db.models.giveaway_entrants import Entrant
from datetime import datetime


def create_new_entrant(
        entrant:EntrantCreate,
        db:Session):
    entrant = Entrant(
        email = entrant.email,
        agree_tos=True,
        date_posted=datetime.now()
    )
    try:
        db.add(entrant)
    except:
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

