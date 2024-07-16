from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                            database='fastapi',
                            user='postgres',
                            password='juanito16',
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "this is our api"}


# Getting all posts
@app.get("/posts", response_model=List[schemas.ResponsePost])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Getting a single post
@app.get("/posts/{id}", response_model=schemas.ResponsePost)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = (
        db.query(models.Post).filter(models.Post.id == id).first()
    )  # filter is like a where statement and stop looking on the first match
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


# Creating a post
@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost
)  # set a response model with the data we want the user to see
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())  # unpack the post dictionary
    db.add(new_post)  # insert into db
    db.commit()  # commit like in psycopg
    db.refresh(new_post)  # like a SQL 'returning *' statement
    return new_post


# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@app.put("/posts/{id}", response_model=schemas.ResponsePost)
async def update_posts(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )  # check there's a post with the id we're looking for
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post_query.update(
        updated_post.model_dump(exclude_unset=True), synchronize_session=False
    )  # update the post with the values we changed
    db.commit()

    return post_query.first()  # return the updated post
