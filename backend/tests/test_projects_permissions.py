from tests.helpers import register_user, login_user, auth_headers

def test_member_cannot_create_project(client):
    email = register_user(client, role="member")
    token = login_user(client, email)

    r = client.post("/projects", json={"name": "P1", "description": "x", "status": "active"}, headers=auth_headers(token))
    assert r.status_code == 403, r.text

def test_manager_can_create_project(client):
    email = register_user(client, role="manager")
    token = login_user(client, email)

    r = client.post("/projects", json={"name": "P1", "description": "x", "status": "active"}, headers=auth_headers(token))
    assert r.status_code in (200, 201), r.text
    assert r.json()["name"] == "P1"
