from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Activity, Organization
from app.schemas import ActivityResponse
from app.services.organization_service import OrganizationService
from app.middleware.auth import verify_api_key

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=List[ActivityResponse], dependencies=[Depends(verify_api_key)])
def get_activities(db: Session = Depends(get_db)):
    """Get all activities"""
    activities = db.query(Activity).filter(Activity.parent_id.is_(None)).all()
    
    def build_activity_tree(activity):
        children = db.query(Activity).filter(Activity.parent_id == activity.id).all()
        return {
            "id": activity.id,
            "name": activity.name,
            "parent_id": activity.parent_id,
            "level": activity.level,
            "children": [build_activity_tree(child) for child in children]
        }
    
    return [build_activity_tree(activity) for activity in activities]


@router.get("/{activity_id}/organizations", response_model=List[dict], dependencies=[Depends(verify_api_key)])
def get_activity_organizations(activity_id: int, db: Session = Depends(get_db)):
    """Get all organizations related to a specific activity (including child activities)"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    service = OrganizationService(db)
    organizations = service.get_organizations_by_activity(activity_id)
    
    result = []
    for org in organizations:
        org_data = {
            "id": org.id,
            "name": org.name,
            "building": {
                "id": org.building.id,
                "address": org.building.address,
                "latitude": org.building.latitude,
                "longitude": org.building.longitude
            },
            "phone_numbers": [phone.number for phone in org.phone_numbers],
            "activities": [{"id": act.id, "name": act.name} for act in org.activities]
        }
        result.append(org_data)
    
    return result