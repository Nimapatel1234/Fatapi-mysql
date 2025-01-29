
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# User model
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    profilepic = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    cellnumber = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    deletedAt = Column(DateTime, nullable=True)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    roleId = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")

# Role model
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")

# AccessToken model
class AccessToken(Base):
    __tablename__ = "accesstoken"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False)
    ttl = Column(Integer, nullable=False)
    userId = Column(Integer, ForeignKey("user.id"))
    created = Column(DateTime, default=datetime.utcnow)
