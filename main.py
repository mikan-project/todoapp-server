from fastapi import FastAPI
from model import Todo
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from db import get_db
from starlette import status
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_todo(db_session: Session, todo_id: int):
    return db_session.query(Todo).filter(Todo.id == todo_id).first()


@app.get("/api/todos")
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@app.post("/api/todos")
async def add(req: Request, db: Session = Depends(get_db)):
    body = await req.json()
    if 'title' not in body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='request body is invalid'
        )
        return
    elif body['title'] == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='request body is empty'
        )
        return
    else:
        element = Todo(
            title=body['title'],
            status="not started"
        )
        db.add(element)
        db.commit()
        return {"detail": "success!"}
    return {}


@app.get("/api/todos/{todo_id}")
async def get(todo_id: int, db: Session = Depends(get_db)):
    element = get_todo(db, todo_id)
    if element is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='todo_id: %s is not found' % todo_id
        )
    else:
        return {"data": element}
    return {}


@app.put("/api/todos/{todo_id}")
async def update(todo_id: int, req: Request, db: Session = Depends(get_db)):
    body = await req.json()
    element = get_todo(db, todo_id)
    if 'title' not in body and 'status' not in body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='request body is invalid'
        )
    elif element is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='todo_id: %s is not found' % todo_id
        )
    else:
        if title in body:
            element.title = body['title']
        if status in body:
            element.status = body['status']
        db.commit()
        return {"message": "success!"}
    return {}


@app.delete("/api/todos/{todo_id}")
async def delete(todo_id: int, db: Session = Depends(get_db)):
    element = get_todo(db, todo_id)
    if element is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='todo_id: %s is not found' % todo_id
        )
    else:
        db.delete(element)
        db.commit()
        return {"message": "success!"}
    return {}
