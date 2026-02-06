from tests.helpers import register_user, login_user

def test_register_and_login(client):
    email = register_user(client, role="member")
    token = login_user(client, email)
    assert token
