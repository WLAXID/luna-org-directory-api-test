from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Organization, Building, Activity, PhoneNumber
from app.schemas import OrganizationResponse, OrganizationSearch
from app.services.organization_service import OrganizationService
from app.middleware.auth import verify_api_key

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=List[dict], dependencies=[Depends(verify_api_key)])
def get_organizations(
    name: Optional[str] = Query(None, description="Search by organization name"),
    activity_id: Optional[int] = Query(None, description="Filter by activity ID"),
    building_id: Optional[int] = Query(None, description="Filter by building ID"),
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Latitude for nearby search"),
    lon: Optional[float] = Query(None, ge=-180, le=180, description="Longitude for nearby search"),
    radius_km: Optional[float] = Query(None, gt=0, description="Radius in kilometers for nearby search"),
    db: Session = Depends(get_db)
):
    """Get organizations with optional filters"""
    service = OrganizationService(db)
    search_params = OrganizationSearch(
        name=name,
        activity_id=activity_id,
        building_id=building_id,
        lat=lat,
        lon=lon,
        radius_km=radius_km
    )
    
    organizations = service.search_organizations(search_params)
    
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


@router.get("/{organization_id}", response_model=dict, dependencies=[Depends(verify_api_key)])
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    """Get organization by ID"""
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return {
        "id": organization.id,
        "name": organization.name,
        "building": {
            "id": organization.building.id,
            "address": organization.building.address,
            "latitude": organization.building.latitude,
            "longitude": organization.building.longitude
        },
        "phone_numbers": [phone.number for phone in organization.phone_numbers],
        "activities": [{"id": act.id, "name": act.name} for act in organization.activities]
    }


@router.get("/search", response_model=List[dict], dependencies=[Depends(verify_api_key)])
def search_organizations_by_name(
    q: str = Query(..., description="Search query for organization name"),
    db: Session = Depends(get_db)
):
    """Search organizations by name"""
    service = OrganizationService(db)
    search_params = OrganizationSearch(name=q)
    organizations = service.search_organizations(search_params)
    
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


@router.get("/nearby", response_model=List[dict], dependencies=[Depends(verify_api_key)])
def get_nearby_organizations(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius_km: float = Query(..., gt=0, description="Radius in kilometers"),
    db: Session = Depends(get_db)
):
    """Get organizations within a specified radius"""
    service = OrganizationService(db)
    search_params = OrganizationSearch(lat=lat, lon=lon, radius_km=radius_km)
    organizations = service.search_organizations(search_params)
    
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