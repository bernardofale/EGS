from typing import Union, Optional
import logging
from fastapi import FastAPI, HTTPException, Query,Header, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, asc
from generateApiKey import generateApiKey
import random
import string

app = FastAPI()


# novas implemetacoes:
    # adicionei sqlalchemy
    # adicionei o campo due date e da para dar Sort by date time or even date
    # adicionei as versoes 1, por agora
    # o delete e o put ja e por id e nao geral.
    # 
    # Por fazer: Adicionar generate Api Key


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Define SQLAlchemy models using SQLAlchemy's ORM (Object-Relational Mapping), sugestao do stor
Base = declarative_base()

class ToDoItem(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    meeting_id = Column(Integer)
    content = Column(Text, nullable=False)
    departamento_id = Column(Integer)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, nullable=False, default=False)
    due_date = Column(Date)

# Create SQLAlchemy engine and session
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://docker:docker@database/exampledb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defining Pydantic models
class ToDoItemCreate(BaseModel):
    description: str
    completed: bool = False
    priority: int = 1
    meeting_id: int
    content: str
    departamento_id: int
    due_date: datetime


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get('/v1/todos', tags=["To-Do"])
async def get_all_todos(
    completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    priority: Optional[int] = Query(None, description="Filter by priority level (1-4)"),
    due_date: Optional[datetime] = Query(None, description="Filter by due date"),
    sort_by_due_date: Optional[str] = Query(None, description="Sort by due date (asc/desc)")
):
    try:
        db = SessionLocal()
        todos = db.query(ToDoItem)
        
        # Filtering
        if completed is not None:
            todos = todos.filter(ToDoItem.completed == completed)
        if priority is not None:
            todos = todos.filter(ToDoItem.priority == priority)
        if due_date is not None:
            todos = todos.filter(ToDoItem.due_date == due_date)
        
        # Sorting
        if sort_by_due_date == "asc":
            todos = todos.order_by(asc(ToDoItem.due_date))
        elif sort_by_due_date == "desc":
            todos = todos.order_by(desc(ToDoItem.due_date))
        
        return {"To-Do List": todos.all()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        db.close()


@app.post('/v1/todos', tags=["To-Do"])
async def create_todo(todo_item: ToDoItemCreate):
    try:
        db = SessionLocal()
        db_todo = ToDoItem(**todo_item.dict())
        db.add(db_todo)
        db.commit()
        return {"message": "To-Do item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create To-Do item: {str(e)}")
    finally:
        db.close()


@app.get('/v1/todos/{todo_id}', tags=["To-Do"])
async def get_todo_by_id(todo_id: int):
    try:
        db = SessionLocal()
        todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
        if todo:
            return todo
        else:
            raise HTTPException(status_code=404, detail="To-Do item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        db.close()

@app.put('/v1/todos/{todo_id}', tags=["To-Do"])
async def update_todo(todo_id: int, todo_item: ToDoItemCreate):
    try:
        db = SessionLocal()
        db_todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
        if db_todo:
            db_todo.description = todo_item.description
            db_todo.completed = todo_item.completed
            db_todo.due_date = todo_item.due_date
            db.commit()
            return {"message": "To-Do item updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="To-Do item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update To-Do item: {str(e)}")
    finally:
        db.close()


@app.delete('/v1/todos/{todo_id}', tags=["To-Do"])
async def delete_todo(todo_id: int):
    try:
        db = SessionLocal()
        todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
        if todo:
            db.delete(todo)
            db.commit()
            return {"message": "To-Do item deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="To-Do item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete To-Do item: {str(e)}")
    finally:
        db.close()