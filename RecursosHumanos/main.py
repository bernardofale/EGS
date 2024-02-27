from fastapi import FastAPI, HTTPException
from models.models import Collaborator

app = FastAPI()

# Mock data for collaborators
collaborators_db = []

@app.get("/v1/collaborators/", tags=["collaborators"], status_code=200)
async def get_all_collaborators() -> list[Collaborator]:
    # Mock function to retrieve all collaborators from the database
    return collaborators_db

@app.get("/v1/collaborators/{collaborator_id}", tags=["collaborators"], status_code=200)
async def get_collaborator(collaborator_id: str) -> Collaborator:
    # Mock function to retrieve collaborator details from the database
    # Replace with actual logic to fetch data from your database
    for collaborator in collaborators_db:
        if collaborator.id == collaborator_id:
            return collaborator
    raise HTTPException(status_code=404, detail="Collaborator not found")

@app.post("/v1/collaborators/", tags=["collaborators"], status_code=201)
async def create_collaborator(collaborator: Collaborator):
    # Mock function to create a new collaborator
    collaborators_db.append(collaborator)
    return {"message": "Collaborator created successfully"}

@app.put("/v1/collaborators/{collaborator_id}", tags=["collaborators"], status_code=200)
async def update_collaborator(collaborator_id: str, updated_collaborator: Collaborator):
    # Mock function to update an existing collaborator
    for i, collaborator in enumerate(collaborators_db):
        if collaborator.id == collaborator_id:
            collaborators_db[i] = updated_collaborator
            return {"message": f"Collaborator {collaborator_id} updated successfully"}
    raise HTTPException(status_code=404, detail="Collaborator not found")

@app.delete("/v1/collaborators/{collaborator_id}", tags=["collaborators"], status_code=204)
async def delete_collaborator(collaborator_id: str):
    # Mock function to delete a collaborator
    for i, collaborator in enumerate(collaborators_db):
        if collaborator.id == collaborator_id:
            del collaborators_db[i]
            return {"message": f"Collaborator {collaborator_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Collaborator not found")