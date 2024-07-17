from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash
from .database import engine, get_db
from .routers import post, user

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
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "this is our api"}
