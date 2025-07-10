from sqlmodel import SQLModel, Field
from typing import List, Optional
import uuid

class DeviceBase(SQLModel, table=True):
    __tablename__ = "devices"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    manufacturer: str = Field(max_length=255)
    model: str = Field(max_length=255)

class DeviceUpdate(DeviceBase):
    manufacturer: Optional[str] = Field(default=None, max_length=255)
    model: Optional[str] = Field(default=None, max_length=255)

class DevicePublic(DeviceBase):
    id: uuid.UUID

class DevicesPublic(SQLModel):
    data: List[DevicePublic]
    count: int