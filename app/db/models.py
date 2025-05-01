from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import json
from sqlalchemy.types import TypeDecorator, TEXT

from .database import Base

# Custom JSON type for SQLite
class JSONType(TypeDecorator):
    impl = TEXT
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None
        
    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    api_name = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    target_standard = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    transformations = relationship("Transformation", back_populates="project", cascade="all, delete-orphan")
    validations = relationship("Validation", back_populates="project", cascade="all, delete-orphan")

class Transformation(Base):
    __tablename__ = "transformations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    source_endpoint = Column(String, nullable=False)
    source_method = Column(String, nullable=False)
    target_endpoint = Column(String, nullable=False)
    target_method = Column(String, nullable=False)
    request_mapping = Column(JSONType)
    response_mapping = Column(JSONType)
    transformation_code = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="transformations")

class Validation(Base):
    __tablename__ = "validations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    schema_id = Column(String, nullable=False)
    is_valid = Column(Boolean, default=False)
    errors = Column(JSONType)
    warnings = Column(JSONType)
    suggestions = Column(JSONType)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="validations")