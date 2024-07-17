from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..utils import hash
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# Creating a new user
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)  # set a response model with the data we want the user to see
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password - user.password
    user.password = hash(user.password)  # update the password

    new_user = models.User(**user.model_dump())  # unpack the post dictionary
    db.add(new_user)  # insert into db
    db.commit()  # commit like in psycopg
    db.refresh(new_user)  # like a SQL 'returning *' statement

    return new_user


# Retrieving a user with a specific id
@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.User).filter(models.User.id == id).first()
    )  # filter is like a where statement and stop looking on the first match
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found",
        )
    return user
