from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Building, Organization
from app.schemas import BuildingResponse
from app.middleware.auth import verify_api_key

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[BuildingResponse], dependencies=[Depends(verify_api_key)])
def get_buildings(db: Session = Depends(get_db)):
    """Get all buildings"""
    buildings = db.query(Building).all()
    return buildings


@router.get("/{building_id}/organizations", response_model=List[dict], dependencies=[Depends(verify_api_key)])
def get_building_organizations(building_id: int, db: Session = Depends(get_db)):
    """Get all organizations in a specific building"""
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    organizations = []
    for org in building.organizations:
        org_data = {
            "id": org.id,
            "name": org.name,
            "phone_numbers": [phone.number for phone in org.phone_numbers],
            "activities": [{"id": act.id, "name": act.name} for act in org.activities]
        }
        organizations.append(org_data)
    
    return organizations