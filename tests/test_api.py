import pytest
from fastapi.testclient import TestClient


class TestAPIEndpoints:
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Organization Directory API", "version": "1.0.0"}

    def test_buildings_endpoint(self, client, auth_headers):
        """Test buildings endpoint."""
        response = client.get("/buildings/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_activities_endpoint(self, client, auth_headers):
        """Test activities endpoint."""
        response = client.get("/activities/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_organizations_endpoint(self, client, auth_headers):
        """Test organizations endpoint."""
        response = client.get("/organizations/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_organization_by_id(self, client, auth_headers):
        """Test getting organization by ID."""
        response = client.get("/organizations/", headers=auth_headers)
        organizations = response.json()
        if organizations:
            org_id = organizations[0]["id"]
            response = client.get(f"/organizations/{org_id}", headers=auth_headers)
            assert response.status_code == 200
            assert "id" in response.json()
            assert "name" in response.json()
        else:
            pytest.skip("No organizations available for testing")

    def test_search_organizations(self, client, auth_headers):
        """Test searching organizations."""
        response = client.get("/organizations/?name=Тест", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_organizations_in_building(self, client, auth_headers):
        """Test getting organizations in building."""
        response = client.get("/buildings/", headers=auth_headers)
        buildings = response.json()
        if buildings:
            building_id = buildings[0]["id"]
            response = client.get(f"/buildings/{building_id}/organizations", headers=auth_headers)
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        else:
            pytest.skip("No buildings available for testing")

    def test_organizations_by_activity(self, client, auth_headers):
        """Test getting organizations by activity."""
        response = client.get("/activities/", headers=auth_headers)
        activities = response.json()
        if activities:
            activity_id = activities[0]["id"]
            response = client.get(f"/activities/{activity_id}/organizations", headers=auth_headers)
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        else:
            pytest.skip("No activities available for testing")

    def test_unauthorized_access(self, client):
        """Test unauthorized access."""
        response = client.get("/organizations/")
        assert response.status_code == 401
        assert "detail" in response.json()

    def test_invalid_api_key(self, client):
        """Test invalid API key."""
        headers = {"Authorization": "Bearer invalid-key"}
        response = client.get("/organizations/", headers=headers)
        assert response.status_code == 401
        assert "detail" in response.json()