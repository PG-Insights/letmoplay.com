"""
Created on Sun May 21 11:06:44 2023

@author: dale
"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from db.session import get_db
from schemas.giveaway_entrants import EntrantCreate, ShowEntrant
from db.repository.giveaway_entrants import create_new_entrant
from db.models.giveaway_entrants import Lmp_Entrant as Entrant

router = APIRouter()


@router.post("/", response_model=ShowEntrant)
def create_entrant(
    entrant: EntrantCreate,
    db: Session = Depends(get_db)
):
    entrant = create_new_entrant(
        entrant=entrant,
        db=db
    )
    return entrant


def remove_entrant(
        entrant_email: str,
        db: Session = Depends(get_db)
) -> dict:
    entrant = db.query(
        Entrant
    ).filter(Entrant.email == entrant_email).first()

    if entrant:
        db.delete(entrant)
        db.commit()
        return {"email": entrant_email}
