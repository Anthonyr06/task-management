from tests.helpers import register_user, login_user, auth_headers

def test_add_comment(client):
    email = register_user(client, role="manager")
    token = login_user(client, email)

    pr = client.post("/projects", json={"name": "P", "description": None, "status": "active"}, headers=auth_headers(token))
    assert pr.status_code in (200, 201), pr.text
    project_id = pr.json()["id"]

    tr = client.post("/tasks", json={
        "project_id": project_id,
        "title": "T",
        "description": None,
        "status": "to_do",
        "priority": "medium",
        "due_date": None,
        "assignee_ids": [],
    }, headers=auth_headers(token))
    task_id = tr.json()["id"]

    cr = client.post(f"/tasks/{task_id}/comments", json={"task_id": task_id, "content": "hola", "mentions": None}, headers=auth_headers(token))
    assert cr.status_code in (200, 201), cr.text

    lr = client.get(f"/tasks/{task_id}/comments", headers=auth_headers(token))
    assert lr.status_code == 200, lr.text
    assert len(lr.json()) >= 1
