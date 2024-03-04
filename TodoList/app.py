from typing import Union
import mysql.connector
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
connection = None
cursor = None

# Defining Pydantic models
class ToDoItem(BaseModel):
    description: str
    completed: bool = False

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
                completed BOOLEAN NOT NULL
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

@app.get('/todos', tags=["To-Do"])
async def get_all_todos():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM todos')
        results = cursor.fetchall()
        return {"To-Do List": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        cursor.close()

@app.post('/todos', tags=["To-Do"])
async def create_todo(todo_item: ToDoItem):
    try:
        cursor = connection.cursor()
        description = todo_item.description
        completed = todo_item.completed

        insert_todo_sql = 'INSERT INTO todos (description, completed) VALUES (%s, %s)'
        cursor.execute(insert_todo_sql, (description, completed))
        connection.commit()

        return {"message": "To-Do item created successfully yesssss"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create To-Do item: {str(e)}")
    finally:
        cursor.close()

@app.get('/todos/{todo_id}', tags=["To-Do"])
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

@app.put('/todos/{todo_id}', tags=["To-Do"])
async def update_todo(todo_id: int, todo_item: ToDoItem):
    try:
        cursor = connection.cursor()
        description = todo_item.description
        completed = todo_item.completed

        update_todo_sql = 'UPDATE todos SET description = %s, completed = %s WHERE id = %s'
        cursor.execute(update_todo_sql, (description, completed, todo_id))
        connection.commit()

        return {"message": "To-Do item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update To-Do item: {str(e)}")
    finally:
        cursor.close()

@app.delete('/todos/{todo_id}', tags=["To-Do"])
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


@app.put('/todos/{todo_id}/complete', tags=["To-Do"], summary="Mark a To-Do Item as Completed")
async def mark_todo_as_completed(todo_id: int):
    try:
        cursor = connection.cursor()
        
        # Check if the To-Do item exists
        cursor.execute('SELECT id FROM todos WHERE id = %s', (todo_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="To-Do item not found")

        # Update the completion status
        update_todo_sql = 'UPDATE todos SET completed = true WHERE id = %s'
        cursor.execute(update_todo_sql, (todo_id,))
        connection.commit()

        return {"message": "To-Do item marked as completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark To-Do item as completed: {str(e)}")
    finally:
        cursor.close()

@app.put('/todos/{todo_id}/incomplete', tags=["To-Do"], summary="Mark a To-Do Item as Incomplete")
async def mark_todo_as_incomplete(todo_id: int):
    try:
        cursor = connection.cursor()
        
        # Check if the To-Do item exists
        cursor.execute('SELECT id FROM todos WHERE id = %s', (todo_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="To-Do item not found")

        # Update the completion status
        update_todo_sql = 'UPDATE todos SET completed = false WHERE id = %s'
        cursor.execute(update_todo_sql, (todo_id,))
        connection.commit()

        return {"message": "To-Do item marked as incomplete successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark To-Do item as incomplete: {str(e)}")
    finally:
        cursor.close()


@app.get('/todos/completed', tags=["To-Do"], summary="Get Completed To-Do Items")
async def get_completed_todos():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM todos WHERE completed = true')
        results = cursor.fetchall()
        return {"Completed To-Do Items": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        cursor.close()

@app.get('/todos/incomplete', tags=["To-Do"], summary="Get Incomplete To-Do Items")
async def get_incomplete_todos():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM todos WHERE completed = false')
        results = cursor.fetchall()
        return {"Incomplete To-Do Items": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")
    finally:
        cursor.close()

