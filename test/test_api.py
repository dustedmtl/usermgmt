# tests/test_api.py

import pytest


# Test user creation
def test_create_user(client):
    response = client.post(
        "/v1/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}


# Test user update
def test_update_user(client):
    # Create a user first to update
    client.post("/v1/users/", json={"username": "updateuser", "email": "update@example.com"})
    
    response = client.put(
        "/v1/users/1",  # Assuming the user ID is 1
        json={"email": "updated@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}


# Test group creation
def test_create_group(client):
    response = client.post(
        "/v1/groups/",
        json={"group_name": "testgroup"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Group added successfully"}


# Test adding user to a group
def test_add_user_to_group(client):
    # Create user and group first

    response = client.post("/v1/groups/1/memberships/", json={"user_id": 1, "role": "member"})  # IDs assumed
    assert response.status_code == 200
    assert response.json() == {"message": "User added to group successfully"}


# Test user deletion
def test_delete_user(client):
    # Create a user first to delete
    # client.post("/v1/users/", json={"username": "deleteuser", "email": "delete@example.com"})

    response = client.delete("/v1/users/1")  # Assuming the user ID is 1
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
