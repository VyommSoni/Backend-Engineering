from fastapi import FastAPI, HTTPException, status
from models import UserRegistrationSchema

app = FastAPI(title="User Registration API")

@app.get("/get_users/v1/data/{username}")
async def get_users_data(username: str):
    # Simulated database check
    if username != "johndoe":
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "username": username,
        "status": "Found"
    }

@app.post("/create_users/v1/register")
async def register_user(payload: UserRegistrationSchema):
    return {
        "register": "Success",
        "status": "Ok",
        "processed_data": payload.model_dump()
    }