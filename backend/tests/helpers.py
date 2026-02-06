from .conftest import rand_email

def register_user(client, role="member", password="Password123!"):
    email = rand_email()
    r = client.post("/auth/register", json={"email": email, "password": password, "role": role})
    assert r.status_code in (200, 201), r.text
    return email

def login_user(client, email, password="Password123!"):
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]

def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}
