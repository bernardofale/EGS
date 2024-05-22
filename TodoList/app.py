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
    # API Key feita.
    # Crio um user com palavra pass nao encriptada, gero uma API Key e dps passo por header essa api key para puder aceder a todos os enpoints, seja get como put e delete.




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Define SQLAlchemy models using SQLAlchemy's ORM (Object-Relational Mapping), sugestao do stor
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    api_key = Column(String(50), unique=True, nullable=False)



class ToDoItem(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    meeting_id = Column(String(50))
    content = Column(Text, nullable=False)
    departamento_id = Column(Integer)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, nullable=False, default=False)
    due_date = Column(Date)

# Create SQLAlchemy engine and session
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://docker:docker@todo_db/exampledb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str


# Defining Pydantic models
class ToDoItemCreate(BaseModel):
    description: str
    completed: bool = False
    priority: int = 1
    meeting_id: str
    content: str
    departamento_id: int
    due_date: datetime


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

def generate_api_key(length: int = 32) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


async def validate_api_key(api_key: Optional[str] = Header(None)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")
    
    db = SessionLocal()
    user = db.query(User).filter(User.api_key == api_key).first()
    db.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")





@app.post('/v1/users', tags=["Users"])
async def create_user(user: UserCreate):
    try:
        db = SessionLocal()
        
        # Check if username already exists
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hash the password (You should use a proper password hashing library like bcrypt)
        # For now, let's assume a simple hashing method
        hashed_password = user.password  # You should replace this with a proper hashing method
        
        # Generate API key
        api_key = generate_api_key()
        
        # Create a new user
        new_user = User(username=user.username, password=hashed_password, api_key=api_key)
        
        db.add(new_user)
        db.commit()
        
        return {"message": "User created successfully", "api_key": api_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    finally:
        db.close()



@app.get('/v1/todos', tags=["To-Do"])
async def get_all_todos(
    completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    priority: Optional[int] = Query(None, description="Filter by priority level (1-4)"),
    due_date: Optional[datetime] = Query(None, description="Filter by due date"),
    sort_by_due_date: Optional[str] = Query(None, description="Sort by due date (asc/desc)"),
    _: None = Depends(validate_api_key)  # Using the dependency here
):
    try:
        db = SessionLocal()
        todos = db.query(ToDoItem)
        
        # Filtering por completed or incompleted, priority 1-4 and due_data
        if completed is not None:
            todos = todos.filter(ToDoItem.completed == completed)
        if priority is not None:
            todos = todos.filter(ToDoItem.priority == priority)
        if due_date is not None:
            todos = todos.filter(ToDoItem.due_date == due_date)
        
        # Sorting asc = ascendente e desc = descendente
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
async def create_todo(
    todo_item: ToDoItemCreate,
    _: None = Depends(validate_api_key)  # Using the dependency here
):
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
async def get_todo_by_id(
    todo_id: int,
    _: None = Depends(validate_api_key)  # Using the dependency here to validade the API Key
):
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


@app.put('/v1/todos/{todo_id}', tags=["To-Do"])
async def update_todo(todo_id: int, todo_item: ToDoItemCreate,
 _: None = Depends(validate_api_key)  # Using the dependency here
):
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
async def delete_todo(
    todo_id: int,
    _: None = Depends(validate_api_key)  # Using the dependency here
):
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


# VER TODAS AS API KEYS GERADAS ATE AGORA:
# @app.get('/v1/users/api_keys', tags=["Users"])
# async def get_all_api_keys():
#     try:
#         db = SessionLocal()
#         users = db.query(User).all()
        
#         # Extract API keys from the users
#         api_keys = [user.api_key for user in users]
        
#         return {"API Keys": api_keys}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve API keys: {str(e)}")
#     finally:
#         db.close()
