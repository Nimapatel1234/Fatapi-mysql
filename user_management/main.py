
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user_management import models, schemas, crud, auth, database
from user_management.auth import verify_token
from typing import List
from datetime import datetime

app = FastAPI()

# Dependency to get current user based on token
def get_current_user(db: Session, token: str = Depends(auth.verify_token)):
    user = db.query(models.User).filter(models.User.id == token.get("sub")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user_management import models, schemas, crud, database
from user_management.auth import get_current_user
from typing import List
from datetime import datetime

app = FastAPI()

# Create user
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

# Get user by ID
@app.get("/api/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.get_user_by_id(db, id)
    if not user or user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return user

# List all users
@app.get("/api/users", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Update user
@app.patch("/api/users/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user_update: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.update_user(db, id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Delete user
@app.delete("/api/users/{id}", response_model=schemas.UserResponse)
def delete_user(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user = crud.delete_user(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Login user
@app.post("/api/users/login", response_model=schemas.Token)
def login_user(login: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, login.cellnumber, login.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generate access token
    token = auth.create_access_token({"sub": str(user.id)})
    
    # Store the token in the database
    ttl = 30 * 60 * 1000  # 30 minutes in milliseconds
    access_token = models.AccessToken(
        token=token,
        ttl=ttl,
        userId=user.id,
        created=datetime.utcnow()
    )
    db.add(access_token)
    db.commit()

    return {"access_token": token, "token_type": "bearer"}   
