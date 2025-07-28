from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.device import Device, DeviceBase, DevicePublic, DevicesPublic
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()

@router.post("/", response_model=DevicePublic)
def create_device(*, session: session_dep, device: DeviceBase):
    db_device = Device.model_validate(device)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return db_device

@router.get("/", response_model=DevicesPublic)
def list_devices(*, session: session_dep):
    devices = session.exec(select(Device)).all()
    return DevicesPublic(data=devices, count=len(devices))

@router.get("/{device_id}", response_model=DevicePublic)
def get_device(*, session: session_dep, device_id: uuid.UUID):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# Come back later and validate device has no repairs tied to it before deleting
@router.delete("/{device_id}", response_model=DevicePublic)
def delete_device(*, session: session_dep, device_id: uuid.UUID):
    pass
    # db_device = session.get(DeviceBase, device_id)
    # if not db_device:
    #     raise HTTPException(status_code=404, detail="Device not found")
    # session.delete(db_device)
    # session.commit()
    # return db_device
