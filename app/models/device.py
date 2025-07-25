from sqlmodel import SQLModel, Field
from typing import List
import uuid

class DeviceBase(SQLModel):
    """Base model for devices"""
    manufacturer: str = Field(nullable=False)
    model: str = Field(nullable=False)

class Device(DeviceBase, table=True):
    """Device model for database"""
    __tablename__ = 'devices'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class DevicePublic(DeviceBase):
    id: uuid.UUID
    manufacturer: str
    model: str

class DevicesPublic(SQLModel):
    data: List[DevicePublic]
    count: int