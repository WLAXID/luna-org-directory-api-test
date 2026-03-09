import pytest
from sqlalchemy.orm import Session
from app.models import Organization, Building, Activity, PhoneNumber

class TestIntegration:
    def test_full_organization_workflow(self, client, auth_headers, db_session, test_building_data, test_organization_name, test_phone_number):
        """Test complete workflow: create building, activity, organization."""
        # Create building
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()

        # Create activity
        activity = Activity(name="Еда", level=1)
        db_session.add(activity)
        db_session.commit()

        # Test organization creation
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        organization.activities.append(activity)
        db_session.add(organization)
        db_session.commit()

        assert organization.id is not None
        assert organization.building_id == building.id
        assert len(organization.activities) == 1
        assert organization.activities[0].id == activity.id

        # Test phone number creation
        phone = PhoneNumber(
            number=test_phone_number,
            organization_id=organization.id
        )
        db_session.add(phone)
        db_session.commit()

        assert phone.id is not None
        assert phone.organization_id == organization.id

    def test_activity_tree_workflow(self, db_session: Session, test_activity_data):
        """Test activity tree structure workflow."""
        # Create root activity
        root = Activity(**test_activity_data)
        db_session.add(root)
        db_session.commit()

        # Create child activities
        child1 = Activity(name="Молочная продукция", level=2, parent_id=root.id)
        child2 = Activity(name="Мясная продукция", level=2, parent_id=root.id)
        db_session.add(child1)
        db_session.add(child2)
        db_session.commit()

        # Verify tree structure
        assert child1.parent_id == root.id
        assert child2.parent_id == root.id
        assert len(root.children) == 2
        assert child1 in root.children
        assert child2 in root.children

    def test_geoposition_workflow(self, db_session: Session, test_building_data, test_building_spb_data):
        """Test geoposition and distance calculation."""
        # Create buildings in different locations
        building1 = Building(**test_building_data)
        building2 = Building(**test_building_spb_data)
        
        db_session.add(building1)
        db_session.add(building2)
        db_session.commit()

        # Create organizations
        org1 = Organization(name="Московская компания", building_id=building1.id)
        org2 = Organization(name="Петербургская компания", building_id=building2.id)
        
        db_session.add(org1)
        db_session.add(org2)
        db_session.commit()

        # Verify coordinates
        assert building1.latitude == test_building_data["latitude"]
        assert building1.longitude == test_building_data["longitude"]
        assert building2.latitude == test_building_spb_data["latitude"]
        assert building2.longitude == test_building_spb_data["longitude"]

    def test_many_to_many_relationships(self, db_session: Session, test_building_data, test_organization_name):
        """Test many-to-many relationships."""
        # Create building
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()

        # Create activities
        activity1 = Activity(name="Еда", level=1)
        activity2 = Activity(name="Технологии", level=1)
        db_session.add(activity1)
        db_session.add(activity2)
        db_session.commit()

        # Create organization
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        organization.activities.extend([activity1, activity2])
        db_session.add(organization)
        db_session.commit()

        # Verify relationships
        assert len(organization.activities) == 2
        assert activity1 in organization.activities
        assert activity2 in organization.activities
        assert len(activity1.organizations) == 1
        assert len(activity2.organizations) == 1
        assert organization in activity1.organizations
        assert organization in activity2.organizations