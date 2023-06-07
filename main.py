from ast import Str
from distutils.log import error
from hashlib import new
from http.client import HTTPException
from random import randrange
from sqlite3 import Cursor
from telnetlib import STATUS
from time import time
from turtle import pos, title
from typing import Optional
from unittest import result
from urllib.error import HTTPError
from xml.sax.handler import property_interning_dict
from xmlrpc.client import boolean
from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi', user= 'postgres', password = 'mibSub073@', 
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\nDatabase connection successfull\n")
        break
    except Exception as error:
        print("\nDatabase connection failed\n")
        print("Error:", error)
        time.sleep(2)

my_posts = [{"title":"titel 1", "content":"content 1", "id": 1}]

class Post(BaseModel):
    title : str
    content : str
    id : int
    created_at: str



def find_posts(id):
    for x in my_posts:
        if x['id'] == id:
            return x

@app.get("/")
def root():
    return {"message": 'hello'}

@app.get("/posts")
def get_data():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"message": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):

    new_dict = post.dict()
    new_dict['id'] = randrange(0,100000)
    my_posts.append(new_dict)

    return {"message": post}


@app.get("/posts/{id}")
def get_one_post(id: int):
    
    result = find_posts(id)
    print(result)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id no {id} is not valid")

    return{"message": result}

def delete_singlepost(id):
    for x in my_posts:
        if x['id'] == id:
            my_posts.remove(x)
            return my_posts

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    result = delete_singlepost(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the url with id no {id} is not valid")

    return {"message": my_posts}

def update_a_post(id, post: Post):
    for x in my_posts:
        if x['id'] == id:
            x['title'] = post.title
            return my_posts


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    result = update_a_post(id, post)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the id {id} is not a valid path")

    return {"message": my_posts}
