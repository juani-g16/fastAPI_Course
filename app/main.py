from turtle import pos
from typing import Optional
from urllib import response
from exceptiongroup import catch
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# schema validation using pydantic
class Post(BaseModel):
    title: str #mandatory
    content: str #mandatory
    published: bool = True #default value


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
@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"message": posts}

# Getting a single post
@app.get("/posts/{id}")
async def get_post(id : int, response : Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# Creating a post
@app.post("/posts",status_code=status.HTTP_201_CREATED) #change default status code
async def create_posts(post : Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
                   RETURNING *""", 
                   (post.title,post.content,post.published)) #avoid use f-string for possible SQL injection
    new_post = cursor.fetchone() #get the recent created post
    
    conn.commit() #push changes to DB

    return {"data" : new_post}

# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@app.put("/posts/{id}")
async def update_posts(id:int, post : Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",     
                    (post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    
    return {"data" : updated_post}
