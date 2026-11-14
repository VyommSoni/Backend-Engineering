"""Session based authentication module for the application.

 Why need?
 Beacuse HTTP is a stateless protocol, so we need to maintain the state of the user across multiple requests. Session-based authentication allows us to store user information on the server side and associate it with a unique session ID, which is sent to the client as a cookie. This way, we can identify the user and maintain their authenticated state throughout their interaction with the application.
 
 Disadvantages of session-based authentication:
    1. Scalability: Session-based authentication can become a bottleneck in large-scale applications, as the server needs to store session data for each user. This can lead to increased memory usage and slower response times.
    #it needs database lookups again and again for each request to validate the session, which can impact performance.
 
 
 how it works?
 
 when client sent a request to the server, the server created a seesion ID and store it in server side storage (like database or in-memory store) along with user information. The server then sends the session ID back to the client as a cookie. For subsequent requests, the client includes the session ID in the cookie, allowing the server to identify the user and maintain their authenticated state."""


from datetime import datetime

from fastapi import FastAPI, Request, Response, HTTPException,Depends,status
from fastapi.security import APIKeyCookie
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Annotated
from uvicorn import run

class UserLogin(BaseModel):
    username: str
    password: str


session_store={} # In-memory session store, you can replace it with a database or any other storage mechanism or redis 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secretpassword"),
        "role": "admin",
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("password123"),
        "role": "user",
    },
}


fastapi = FastAPI(title="Session-Based-Authentication")


cookie_scheme=APIKeyCookie(name="session_id", auto_error=False) # extract session_id from cookie, if not found then return None instead of raising an error


@fastapi.post("/auth/session/login")
def login(user:UserLogin,response:Response):
    """
    User login endpoint. Validates user credentials and creates a session.
    """
    user_data=fake_users_db.get(user.username)
    if not user_data or not pwd_context.verify(user.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    #if found create session ID and store it in session_store 
    session_id = f"sess_{user.username}_{datetime.now().timestamp()}"
    session_store[session_id] = {"username": user.username, "role": user_data["role"]}

    #set http-only cookie 
    response.set_cookie(key="session_id",value=session_id,httponly=True)

    return {
        "message": "Login successful",
        "session_id": session_id,
        "user": {"username": user.username, "role": user_data["role"]},
    }



def get_current_user(session_id:Annotated[str | None, Depends(cookie_scheme)]):
    """This function retrieves the current user based on the session ID stored in the cookie."""
    if not session_id or not session_id in session_store:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    username=session_store[session_id]
    return {"username": fake_users_db[username]["username"], "role": fake_users_db[username]["role"]}

@fastapi.get("/profile/session")
def protected_route(current_user:Annotated[dict,Depends(get_current_user)]):
    """This function is a protected route that requires authentication."""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")

    return {
        "auth_type":"session-based",
        "username":  current_user['username'],
        "role":current_user['role'],
        }

@fastapi.post("/auth/session/logout")
def logout(response:Response,session_id:Annotated[str | None, Depends(cookie_scheme)]):
    """This function logs out the user by deleting the session ID from the session store and clearing the cookie."""
    if not session_id or not session_id in session_store:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    #delete session from store
    del session_store[session_id]

    #clear cookie
    response.delete_cookie(key="session_id")

    return {"message": "Logout successful"}

if __name__ == "__main__":
    run(fastapi, host="127.0.0.1", port=8000)