from enum import IntEnum
from datetime import date, datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel

class RepairStatus(IntEnum):
    """Enum for repair status values"""
    OPEN = 1
    PENDING = 2
    CLOSED = 3

class RepairBase(SQLModel):
    """Base model for repairs"""
    status:                 RepairStatus        = Field(nullable=False, default=RepairStatus.OPEN,                                description="Status of the repair", sa_column_kwargs={"server_default": str(RepairStatus.OPEN.value)})
    external_ticket_number: Optional[str]       = Field(nullable=True,  default=None,                                             description="External ticket number for the repair")

class Repair(RepairBase, table=True):
    """Table model for repairs"""
    id:                     uuid.UUID           = Field(nullable=False, default_factory=uuid.uuid4, primary_key=True,             description="Unique identifier for the repair")
    creator_id:             uuid.UUID           = Field(nullable=False, default_factory=None,       foreign_key="users.id",       description="ID of the user who created the repair")
    created_at:             datetime            = Field(nullable=False, default_factory=date.today,                               description="Date the repair was created")
    updated_at:             datetime            = Field(nullable=False, default_factory=date.today,                               description="Date the repair was last updated")
    date_raised:            date                = Field(nullable=False, default_factory=None,                                     description="Date the repair was raised")
    date_closed:            Optional[date]      = Field(nullable=True,  default=None,                                             description="Date the repair was closed")
    school_id:              uuid.UUID           = Field(nullable=False, default_factory=None,       foreign_key="schools.id",     description="ID of the school associated with the repair")
    device_serial:          str                 = Field(nullable=False, default_factory=None,                                     description="Serial number of the device associated with the repair")
    device_model_id:        uuid.UUID           = Field(nullable=False, default_factory=None,       foreign_key="devices.id",     description="ID of the device model associated with the repair")
    has_protective_case:    bool                = Field(nullable=False, default_factory=None,                                     description="Whether the device has a protective case")
    is_sla_breached:        bool                = Field(nullable=False, default=False,                                            description="Whether the SLA for the repair has been breached")
    inbound_collection_id:  Optional[uuid.UUID] = Field(nullable=True,  default=None,               foreign_key="collections.id", description="ID of the inbound collection associated with the repair")
    outbound_collection_id: Optional[uuid.UUID] = Field(nullable=True,  default=None,               foreign_key="collections.id", description="ID of the outbound collection associated with the repair")
    inbound_date:           Optional[date]      = Field(nullable=True,  default=None,                                             description="Date the inbound collection was received")
    outbound_date:          Optional[date]      = Field(nullable=True,  default=None,                                             description="Date the outbound collection was sent")

class RepairCreate(RepairBase):
    """Model for creating a repair"""
    school_id:              uuid.UUID           = Field(nullable=False,                             foreign_key="schools.id",     description="ID of the school associated with the repair")
    device_serial:          str                 = Field(nullable=False,                                                           description="Serial number of the device associated with the repair")
    device_model_id:        uuid.UUID           = Field(nullable=False,                             foreign_key="devices.id",     description="ID of the device model associated with the repair")
    has_protective_case:    bool                = Field(nullable=False,                                                           description="Whether the device has a protective case")

class RepairUpdate(RepairBase):
    """Model for updating a repair"""
    date_closed:            Optional[date]      = Field(default=None,                                                             description="Date the repair was closed")
    inbound_collection_id:  Optional[uuid.UUID] = Field(default=None,                               foreign_key="collections.id", description="ID of the inbound collection associated with the repair")
    outbound_collection_id: Optional[uuid.UUID] = Field(default=None,                               foreign_key="collections.id", description="ID of the outbound collection associated with the repair")
    inbound_date:           Optional[date]      = Field(default=None,                                                             description="Date the inbound collection was received")
    outbound_date:          Optional[date]      = Field(default=None,                                                                 description="Date the outbound collection was sent")

class RepairPublic(RepairBase):
    """Public model for a repair"""
    id: uuid.UUID
    creator_id: uuid.UUID
    updated_at: datetime
    created_at: datetime
    date_raised: date
    date_closed: Optional[date] = None
    school_id: uuid.UUID
    device_serial: str
    device_model_id: uuid.UUID
    has_protective_case: bool
    is_sla_breached: bool
    inbound_collection_id: Optional[uuid.UUID] = None
    outbound_collection_id: Optional[uuid.UUID] = None
    inbound_date: Optional[date] = None
    outbound_date: Optional[date] = None

class RepairsPublic(SQLModel):
    """Public model for a list of repairs"""
    data: list[RepairPublic]
    count: int