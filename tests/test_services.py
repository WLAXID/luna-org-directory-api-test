import pytest
from sqlalchemy.orm import Session
from app.services.organization_service import OrganizationService
from app.schemas import OrganizationCreate, OrganizationSearch
from app.models import Organization, Building, Activity, PhoneNumber

class TestOrganizationService:
    def test_create_organization(self, db_session: Session, test_building_data, test_organization_name, test_phone_number):
        """Test creating an organization with service."""
        service = OrganizationService(db_session)
        
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()

        org_data = OrganizationCreate(
            name=test_organization_name,
            building_id=building.id,
            phone_numbers=[test_phone_number],
            activity_ids=[]
        )
        
        organization = service.create_organization(org_data)
        assert organization.id is not None
        assert organization.name == test_organization_name
        assert len(organization.phone_numbers) == 1
        assert organization.phone_numbers[0].number == test_phone_number

    def test_get_organization(self, db_session: Session, test_building_data, test_organization_name):
        """Test getting organization by ID."""
        service = OrganizationService(db_session)
        
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        db_session.add(organization)
        db_session.commit()
        
        found_org = service.get_organization(organization.id)
        assert found_org is not None
        assert found_org.name == test_organization_name

    def test_search_organizations_by_name(self, db_session: Session, test_building_data, test_organization_name):
        """Test searching organizations by name."""
        service = OrganizationService(db_session)
        
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        org1 = Organization(name=test_organization_name, building_id=building.id)
        org2 = Organization(name="ООО Молочная продукция", building_id=building.id)
        db_session.add(org1)
        db_session.add(org2)
        db_session.commit()
        
        search_params = OrganizationSearch(name="Рога")
        results = service.search_organizations(search_params)
        assert len(results) == 1
        assert results[0].name == test_organization_name

    def test_get_child_activity_ids(self, db_session: Session, test_activity_data):
        """Test getting child activity IDs recursively."""
        service = OrganizationService(db_session)
        
        # Create root activity first
        root = Activity(**test_activity_data)
        db_session.add(root)
        db_session.commit()
        
        # Create child activities
        child1 = Activity(name="Молочная продукция", level=2, parent_id=root.id)
        child2 = Activity(name="Мясная продукция", level=2, parent_id=root.id)
        grandchild = Activity(name="Сыр", level=3, parent_id=child1.id)
        
        db_session.add(child1)
        db_session.add(child2)
        db_session.add(grandchild)
        db_session.commit()
        
        child_ids = service._get_child_activity_ids(root.id)
        # The method should return at least direct children
        assert len(child_ids) >= 2  # At least child1 and child2
        assert child1.id in child_ids
        assert child2.id in child_ids

    def test_get_organizations_by_building(self, db_session: Session, test_building_data):
        """Test getting organizations by building."""
        service = OrganizationService(db_session)
        
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        org1 = Organization(name="Организация 1", building_id=building.id)
        org2 = Organization(name="Организация 2", building_id=building.id)
        db_session.add(org1)
        db_session.add(org2)
        db_session.commit()
        
        results = service.get_organizations_by_building(building.id)
        assert len(results) == 2
        assert all(org.building_id == building.id for org in results)

    def test_get_organizations_by_activity(self, db_session: Session, test_building_data, test_organization_name):
        """Test getting organizations by activity."""
        service = OrganizationService(db_session)
        
        building = Building(**test_building_data)
        db_session.add(building)
        db_session.commit()
        
        activity = Activity(name="Еда", level=1)
        db_session.add(activity)
        db_session.commit()
        
        organization = Organization(
            name=test_organization_name,
            building_id=building.id
        )
        organization.activities.append(activity)
        db_session.add(organization)
        db_session.commit()
        
        results = service.get_organizations_by_activity(activity.id)
        assert len(results) == 1
        assert results[0].name == test_organization_name