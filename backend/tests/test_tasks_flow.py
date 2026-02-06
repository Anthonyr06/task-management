from tests.helpers import register_user, login_user, auth_headers

def test_create_task_with_assignees(client):
    # manager crea proyecto y tarea
    mgr_email = register_user(client, role="manager")
    mgr_token = login_user(client, mgr_email)

    # crea un member para asignarlo
    mem_email = register_user(client, role="member")
    mem_token = login_user(client, mem_email)

    # obtener UUID del member via /users/me
    me = client.get("/users/me", headers=auth_headers(mem_token))
    assert me.status_code == 200, me.text
    member_id = me.json()["id"]

    # crear proyecto
    pr = client.post("/projects", json={"name": "PX", "description": None, "status": "active"}, headers=auth_headers(mgr_token))
    assert pr.status_code in (200, 201), pr.text
    project_id = pr.json()["id"]

    # crear task con assignee_ids
    tr = client.post("/tasks", json={
        "project_id": project_id,
        "title": "T1",
        "description": "d",
        "status": "to_do",
        "priority": "high",
        "due_date": None,
        "assignee_ids": [member_id],
    }, headers=auth_headers(mgr_token))
    assert tr.status_code in (200, 201), tr.text
    task = tr.json()
    assert task["title"] == "T1"
    assert len(task["assignees"]) == 1
