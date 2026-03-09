import pytest
from sqlalchemy.orm import Session
from app.models import Organization, Building, Activity, PhoneNumber
from app.database import Base

class TestModels:
    def test_building_creation(self, db_session: Session, test_building_data):
        """Test building model creation."""
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        assert building.id is not None
        assert building.address == test_building_data["address"]
        assert building.latitude == test_building_data["latitude"]
        assert building.longitude == test_building_data["longitude"]

    def test_organization_creation(self, db_session: Session, test_building_data, test_organization_name):
        """Test organization model creation."""
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        db_session.add(organization)
        db_session.commit()
        
        assert organization.id is not None
        assert organization.name == test_organization_name
        assert organization.building_id == building.id

    def test_activity_creation(self, db_session: Session, test_activity_data):
        """Test activity model creation."""
        activity = Activity(**test_activity_data)
        db_session.add(activity)
        db_session.commit()
        
        assert activity.id is not None
        assert activity.name == test_activity_data["name"]
        assert activity.level == test_activity_data["level"]

    def test_phone_number_creation(self, db_session: Session, test_building_data, test_organization_name, test_phone_number):
        """Test phone number model creation."""
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        db_session.add(organization)
        db_session.commit()
        
        phone = PhoneNumber(number=test_phone_number, organization_id=organization.id)
        db_session.add(phone)
        db_session.commit()
        
        assert phone.id is not None
        assert phone.number == test_phone_number
        assert phone.organization_id == organization.id

    def test_activity_tree_structure(self, db_session: Session, test_activity_data):
        """Test activity tree structure."""
        root = Activity(**test_activity_data)
        child = Activity(name="Молочная продукция", level=2)
        root.children.append(child)
        
        db_session.add(root)
        db_session.add(child)
        db_session.commit()
        
        assert child.parent_id == root.id
        assert len(root.children) == 1
        assert root.children[0].name == "Молочная продукция"

    def test_organization_activities_relationship(self, db_session: Session, test_building_data, test_organization_name):
        """Test many-to-many relationship between organizations and activities."""
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        activity1 = Activity(name="Еда", level=1)
        activity2 = Activity(name="Молочная продукция", level=2)
        
        db_session.add(organization)
        db_session.add(activity1)
        db_session.add(activity2)
        db_session.commit()
        
        organization.activities.extend([activity1, activity2])
        db_session.commit()
        
        assert len(organization.activities) == 2
        assert activity1 in organization.activities
        assert activity2 in organization.activities