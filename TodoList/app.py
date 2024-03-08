from typing import Union
import mysql.connector
import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
connection = None
cursor = None

# Defining Pydantic models
class ToDoItem(BaseModel):
    description: str
    completed: bool = False
    priority: int = 1
    meeting_id: int
    content: str
    Departamento_id: int
    due_date: datetime  

@app.on_event("startup")
async def startup_event():
    while not connect_db():
        continue

def create_tables():
    try:
        global connection, cursor

        create_todo_table = """
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description TEXT NOT NULL,
                meeting_id VARCHAR(50),
                content TEXT NOT NULL,
                departamento_id VARCHAR(50),
                priority INT DEFAULT 1,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                due_date DATE  # Added due_date column
            )
        """
        cursor = connection.cursor()
        cursor.execute(create_todo_table)

        connection.commit()
        logger.info("Tables created successfully in MySQL database")
    except (mysql.connector.Error) as error:
        logger.error(f"Error while creating MySQL tables: {error}")
        return False

def connect_db():
    global connection, cursor
    try:
        connection = mysql.connector.connect(
            user="docker",
            password="docker",
            host="database",
            database="exampledb"
        )

        cursor = connection.cursor()
        if connection:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            logger.info(f"Connected to {db_version[0]}")
            create_tables()
            return True
        else:
            logger.error("Failed to connect to the database.")
            return False
    except (mysql.connector.Error) as error:
        logger.error(f"Error while connecting to MySQL: {error}")
        return False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/v1/todos', tags=["To-Do"])
async def get_all_todos(completed: Union[bool, None] = Query(None, description="Filter by completion status (true/false)"), priority: Union[int, None] = Query(None, description="Filter by priority level (1-4)")):
    try:
        cursor = connection.cursor(dictionary=True)
        if completed is not None and priority is not None:
            cursor.execute('SELECT * FROM todos WHERE completed = %s AND priority = %s', (completed, priority))
        elif completed is not None:
            cursor.execute('SELECT * FROM todos WHERE completed = %s', (completed,))
        elif priority is not None:
            cursor.execute('SELECT * FROM todos WHERE priority = %s', (priority,))
        else:
            cursor.execute('SELECT * FROM todos')
        results = cursor.fetchall()
        return {"To-Do List": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        cursor.close()

@app.post('/v1/todos', tags=["To-Do"])
async def create_todo(todo_item: ToDoItem):
    try:
        cursor = connection.cursor()
        description = todo_item.description
        completed = todo_item.completed
        priority = todo_item.priority
        departamento_id = todo_item.Departamento_id
        content = todo_item.content
        meeting_id = todo_item.meeting_id
        due_date = todo_item.due_date  

        insert_todo_sql = 'INSERT INTO todos (description, completed, priority, departamento_id, content, meeting_id, due_date) VALUES (%s, %s, %s, %s, %s, %s, %s)'  
        cursor.execute(insert_todo_sql, (description, completed, priority, departamento_id, content, meeting_id, due_date))
        connection.commit()

        return {"message": "To-Do item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create To-Do item: {str(e)}")
    finally:
        cursor.close()

@app.get('/v1/todos/{todo_id}', tags=["To-Do"])
async def get_todo_by_id(todo_id: int):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="To-Do item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        cursor.close()

@app.put('/v1/todos/{todo_id}', tags=["To-Do"])
async def update_todo(todo_id: int, todo_item: ToDoItem):
    try:
        cursor = connection.cursor()
        description = todo_item.description
        completed = todo_item.completed
        due_date = todo_item.due_date  

        update_todo_sql = 'UPDATE todos SET description = %s, completed = %s, due_date = %s WHERE id = %s'  
        cursor.execute(update_todo_sql, (description, completed, due_date, todo_id))
        connection.commit()

        return {"message": "To-Do item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update To-Do item: {str(e)}")
    finally:
        cursor.close()

@app.delete('/v1/todos/{todo_id}', tags=["To-Do"])
async def delete_todo(todo_id: int):
    try:
        cursor = connection.cursor()
        delete_todo_sql = 'DELETE FROM todos WHERE id = %s'
        cursor.execute(delete_todo_sql, (todo_id,))
        connection.commit()

        return {"message": "To-Do item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete To-Do item: {str(e)}")
    finally:
        cursor.close()

