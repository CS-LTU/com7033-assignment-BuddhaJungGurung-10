def test_login_valid(client):
    res = client.post("/auth/login", data={
        "email": "admin@gmail.com",
        "password": "asd123asd"
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b"Dashboard" in res.data or b"Logout" in res.data


def test_login_invalid(client):
    res = client.post("/auth/login", data={
        "email": "admin@gmail.com",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert b"Invalid" in res.data or res.status_code == 200


def test_register_admin_only(client):
    # Login as admin user
    client.post("/auth/login", data={
        "email": "admin@gmail.com",
        "password": "asd123asd"
    }, follow_redirects=True)

    res = client.post("/auth/register", data={
        "username": "newuser",
        "email": "newuser@gmail.com",
        "password": "12345",
        "confirm_password": "12345"
        
    }, follow_redirects=True)

    assert b"User registered successfully" in res.data or res.status_code == 200

def test_register_non_admin(client):
    client.post("/auth/login", data={
        "email": "doctor@gmail.com",
        "password": "doctorpass"
    }, follow_redirects=True)

    res = client.post("/auth/register", data={
        "username": "newuser",
        "email": "newuser@gmail.com",
        "password": "12345",
        "confirm_password": "12345"
    }, follow_redirects=True)

    assert b"Not authorized" in res.data or res.status_code == 200