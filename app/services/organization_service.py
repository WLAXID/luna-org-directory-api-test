from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
import math
from app.models import Organization, Building, Activity, PhoneNumber
from app.schemas import OrganizationCreate, OrganizationSearch


class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def create_organization(self, org_data: OrganizationCreate) -> Organization:
        organization = Organization(
            name=org_data.name,
            building_id=org_data.building_id
        )
        self.db.add(organization)
        self.db.flush()

        # Add phone numbers
        for phone in org_data.phone_numbers:
            phone_obj = PhoneNumber(number=phone, organization_id=organization.id)
            self.db.add(phone_obj)

        # Add activities
        if org_data.activity_ids:
            activities = self.db.query(Activity).filter(Activity.id.in_(org_data.activity_ids)).all()
            organization.activities.extend(activities)

        self.db.commit()
        self.db.refresh(organization)
        return organization

    def get_organization(self, org_id: int) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def search_organizations(self, search_params: OrganizationSearch) -> List[Organization]:
        query = self.db.query(Organization)

        if search_params.name:
            query = query.filter(Organization.name.ilike(f"%{search_params.name}%"))

        if search_params.building_id:
            query = query.filter(Organization.building_id == search_params.building_id)

        if search_params.activity_id:
            # Get all child activities recursively
            child_activity_ids = self._get_child_activity_ids(search_params.activity_id)
            query = query.join(Organization.activities).filter(Activity.id.in_(child_activity_ids))

        if search_params.lat and search_params.lon and search_params.radius_km:
            query = self._filter_by_distance(
                query, search_params.lat, search_params.lon, search_params.radius_km
            )

        return query.all()

    def get_organizations_by_building(self, building_id: int) -> List[Organization]:
        return self.db.query(Organization).filter(Organization.building_id == building_id).all()

    def get_organizations_by_activity(self, activity_id: int) -> List[Organization]:
        child_activity_ids = self._get_child_activity_ids(activity_id)
        return (
            self.db.query(Organization)
            .join(Organization.activities)
            .filter(Activity.id.in_(child_activity_ids))
            .all()
        )

    def _get_child_activity_ids(self, activity_id: int) -> List[int]:
        """Get all child activity IDs recursively (max 3 levels)"""
        activity_ids = [activity_id]
        
        # Level 1 children
        level1 = self.db.query(Activity.id).filter(Activity.parent_id == activity_id).all()
        activity_ids.extend([a[0] for a in level1])
        
        # Level 2 children
        if level1:
            level1_ids = [a[0] for a in level1]
            level2 = self.db.query(Activity.id).filter(Activity.parent_id.in_(level1_ids)).all()
            activity_ids.extend([a[0] for a in level2])
            
            # Level 3 children
            if level2:
                level2_ids = [a[0] for a in level2]
                level3 = self.db.query(Activity.id).filter(Activity.parent_id.in_(level2_ids)).all()
                activity_ids.extend([a[0] for a in level3])
        
        return list(set(activity_ids))

    def _filter_by_distance(self, query, lat: float, lon: float, radius_km: float):
        """Filter organizations by distance using Haversine formula"""
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert degrees to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Calculate distance using Haversine formula
        distance_expr = (
            R * 2 * func.asin(
                func.sqrt(
                    func.pow(func.sin((func.radians(Building.latitude) - lat_rad) / 2), 2) +
                    func.cos(func.radians(Building.latitude)) * func.cos(lat_rad) *
                    func.pow(func.sin((func.radians(Building.longitude) - lon_rad) / 2), 2)
                )
            )
        )
        
        return query.join(Building).filter(distance_expr <= radius_km)