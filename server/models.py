from fastapi import Request
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, event, Enum
from database import Base
from utility import RoleType

class BaseModel(Base):
    __abstract__ = True  # Ensures this class is not treated as a table
    __allow_unmapped__ = True  # Allows using old-style Column()
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

@event.listens_for(Base, 'before_insert', propagate = True)
def before_insert(mapper, connection, target):

    target.created_at = datetime.utcnow()
    target.updated_at = datetime.utcnow()
    target.created_by = 1  # Replc ace with actual user logic
    target.updated_by = 1

@event.listens_for(Base, 'before_update', propagate = True)
def before_update(mapper, connection, target):
    target.updated_at = datetime.utcnow()
    target.updated_by = 1 # Replace with actual user logic


class UserTokenModel(Base):
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    user_token = Column(String(255), unique=True)
    is_revoked = Column(Boolean, unique=False, default=False)

class UserModel(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), unique=False)
    lastname = Column(String(100), unique=False)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(256))
    role = Column(Enum(RoleType), nullable=False)
    active_user = Column(Boolean, unique=False, default=True)
    is_deleted = Column(Boolean, unique=False, default=False)