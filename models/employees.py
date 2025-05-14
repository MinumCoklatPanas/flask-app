from uuid import uuid4

from sqlalchemy import Column, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, TEXT, INTEGER
from .base import BaseModel

class Employees(BaseModel):
  __tablename__ = 'employees'

  id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
  name = Column(TEXT)
  age = Column(INTEGER)
  email = Column(TEXT)
  created_at = Column(TIMESTAMP(timezone=True), default=func.now())
  updated_at = Column(TIMESTAMP(timezone=True), default=func.now())

  def as_dict(self):
    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}