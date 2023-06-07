from dis import Positions
import imp
from sqlite3 import Cursor
from statistics import mode
from turtle import title
from urllib import response
from fastapi import FastAPI, status, HTTPException, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel
from fastapi.params import Body

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',port = '5432',database = 'fastapi', user = 'postgres', password = 'mibSub073@',
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("\nDatabase connection successfull\n")
        break
    except Exception as error:
        print("\nDatabase connection failed\n")
        print("Error:", error)
        time.sleep(2)

class Post(BaseModel):
    title : str
    content: str

@app.get("/posts")
def get_data():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"message": posts}

@app.get("/posts/{id}")
def get_single_post(id : int):
    cursor.execute("""select * from posts where id = %s""", (str(id)))
    single_post = cursor.fetchone()
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the url with id {id} is not valid")
    return{"message": single_post}
    

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def inser_posts(post :  Post):
    cursor.execute("""insert into posts(name,content) values(%s,%s) returning *""", (post.title, post.content))
    new_post = cursor.fetchone()
    conn.commit()
    return{"message": new_post}


@app.delete("/posts/{id}")
def delete_posts(id: int):
    cursor.execute("""delete from posts where id = %s returning * """, (str(id)))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    cursor.execute("""update posts set name = %s where id = %s returning *""", (post.title ,str(id)))
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the url with id {id} is not valid")
    conn.commit()
    return {"message": updated_post}