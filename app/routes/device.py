from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.models.device import Device, DeviceBase, DevicePublic, DevicesPublic
from app.models.repair import Repair
from app.utils.dependencies import session_dep
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#
# Device view routes and HTMX Partials
#

@router.get("/overview", response_class=HTMLResponse)
def device_overview(*, session: session_dep, request: Request):
    devices = session.exec(select(Device)).all()
    return templates.TemplateResponse(
        "components/device_overview.html",
        {"request": request, "devices": devices}
    )

#
# Device CRUD routes
#

@router.post("/", response_class=HTMLResponse)
def create_device(*, request: Request, session: session_dep, device: Annotated[DeviceBase, Form()]):
    db_device = Device.model_validate(device)
    session.add(db_device)
    session.commit()
    session.refresh(db_device)
    return templates.TemplateResponse(
        name="components/notification.html",
        context={"request": request, "message": "Device created successfully!", "type": "success"},
        headers={"HX-Trigger": "refreshOverview"},
        status_code=status.HTTP_201_CREATED
    )
    # return HTMLResponse(
    #     status_code=status.HTTP_201_CREATED,
    #     headers={
    #         "HX-Trigger": "refreshOverview"
    #     }
    # )

# Not in use yet
# @router.get("/{device_id}", response_model=DevicePublic)
# def get_device(*, session: session_dep, device_id: uuid.UUID):
#     device = session.get(Device, device_id)
#     if not device:
#         raise HTTPException(status_code=404, detail="Device not found")
#     return device

# Come back later and validate device has no repairs tied to it before deleting
@router.delete("/{device_id}", response_model=DevicePublic)
def delete_device(*, request: Request, session: session_dep, device_id: uuid.UUID):
    associated_repairs = session.exec(
        select(Repair).where(Repair.device_model_id == device_id)
    ).all()

    if associated_repairs:
        return templates.TemplateResponse(
            "components/notification.html",
            {"request": request, "message": "Cannot delete a device model with associated repairs!", "type": "error"}
        )
    
    db_device = session.get(Device, device_id)
    if not db_device:
        return templates.TemplateResponse(
            name="components/notification.html",
            context={"request": request, "message": "Cannot delete a device that does not exist!", "type": "error"}
        )
    
    session.delete(db_device)
    session.commit()
    return templates.TemplateResponse(
        name="components/notification.html",
        context={"request": request, "message": "Device deleted successfully!", "type": "success"},
        headers={"HX-Trigger": "refreshOverview"}
    )