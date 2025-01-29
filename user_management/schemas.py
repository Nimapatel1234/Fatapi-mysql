
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Role schema
class RoleBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# User schema
class UserBase(BaseModel):
    name: str
    cellnumber: str
    email: str
    profilepic: Optional[str] = None
    deletedAt: Optional[datetime] = None
    created: datetime
    modified: datetime
    roleId: int

    class Config:
        from_attributes = True

# UserCreate schema - for POST request to create a new user
class UserCreate(UserBase):
    password: str  # Only needed during user creation

# UserResponse schema - for GET request to return user info
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# LoginRequest schema - for POST request during login
class LoginRequest(BaseModel):
    cellnumber: str
    password: str

    class Config:
        from_attributes = True

# Token schema - the response after login
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

# AccessToken schema - for storing tokens in the database
class AccessTokenBase(BaseModel):
    token: str
    ttl: int
    userId: int
    created: datetime

    class Config:
        from_attributes = True
        
from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    profilepic: Optional[str]
    name: Optional[str]
    email: Optional[str]

