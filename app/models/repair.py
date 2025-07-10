from enum import IntEnum
from .school import SchoolPublic
from .device import DevicePublic
from .collection import CollectionPublic
from .user import UserPublic

from datetime import date, datetime
from sqlmodel import SQLModel, Field
from typing import List, Optional 
import uuid

class RepairBase(SQLModel, table=True):
    """Base model for repairs"""
    __tablename__ = "repairs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    date_raised: date
    school_id: uuid.UUID
    device_serial: str = Field(max_length=255)
    device_model_id: uuid.UUID
    has_protective_case: bool = True
    external_ticket_number: Optional[str] = Field(default=None, max_length=100)

class RepairCreate(RepairBase):
    pass

class RepairUpdate(SQLModel):
    status: Optional[int] = Field(default=None, ge=1, le=10)  # Assuming status range
    date_closed: Optional[date] = Field(default=None)
    school_id: Optional[uuid.UUID] = Field(default=None)
    device_serial: Optional[str] = Field(default=None, max_length=255)
    device_model_id: Optional[uuid.UUID] = Field(default=None)
    has_protective_case: Optional[bool] = Field(default=None)
    external_ticket_number: Optional[str] = Field(default=None, max_length=100)
    is_sla_breached: Optional[bool] = Field(default=None)
    inbound_collection_id: Optional[uuid.UUID] = Field(default=None)
    outbound_collection_id: Optional[uuid.UUID] = Field(default=None)
    inbound_date: Optional[date] = Field(default=None)
    outbound_date: Optional[date] = Field(default=None)

class RepairPublic(RepairBase):
    id: uuid.UUID
    status: int
    creator_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    date_closed: Optional[date]
    is_sla_breached: bool
    inbound_collection_id: Optional[uuid.UUID]
    outbound_collection_id: Optional[uuid.UUID]
    inbound_date: Optional[date]
    outbound_date: Optional[date]

class RepairWithRelations(RepairPublic):
    """Extended repair model that includes related objects"""
    creator: Optional["UserPublic"] = None
    school: Optional[SchoolPublic] = None
    device_model: Optional[DevicePublic] = None
    inbound_collection: Optional[CollectionPublic] = None
    outbound_collection: Optional[CollectionPublic] = None

class RepairsPublic(SQLModel):
    data: List[RepairPublic]
    count: int

class RepairStatus(IntEnum):
    """Enum for repair status values"""
    OPEN = 1
    CLOSED = 2
    # Add other status values as needed

# Special action models for repair workflow
class RepairStatusUpdate(SQLModel):
    status: int = Field(ge=1, le=10)
    date_closed: Optional[date] = Field(default=None)

class RepairCollectionAssignment(SQLModel):
    inbound_collection_id: Optional[uuid.UUID] = Field(default=None)
    outbound_collection_id: Optional[uuid.UUID] = Field(default=None)
    inbound_date: Optional[date] = Field(default=None)
    outbound_date: Optional[date] = Field(default=None)