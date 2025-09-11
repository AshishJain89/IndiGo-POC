from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# Dummy user for demonstration
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == VALID_USERNAME
    correct_password = credentials.password == VALID_PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
