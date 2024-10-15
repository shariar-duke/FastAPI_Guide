from typing import Optional
from fastapi import  FastAPI, Response,status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool = True



# Establish database connection
try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="duke123", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection to database failed")
    print("Error:", error)



my_posts =[{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"title of post 2", "content":"content of post 2", "id":2},{"title":"title of post 3", "content":"content of post 3", "id":3}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):  # i is the index, p is the post
        if p['id'] == id:
            return i

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return{ "data" : posts }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

 


@app.get("/posts/{id}")
def get_post(id:int , response:Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return {"post_details": post}

# DELETE a post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s returning  *""", (id,))
    deleted_post =  cursor.fetchone()
    conn.commit()

    # Handle the case where the post is not found
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    # Return a 204 No Content response (optional since it's already set in the decorator)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, id)
    )

    updated_post = cursor.fetchone()
    # Save the changes
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return {"data": updated_post}
