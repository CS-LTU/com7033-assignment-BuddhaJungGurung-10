sample_patient = {
    "id": 1001,
    "gender": "Male",
    "age": 45,
    "hypertension": 0,
    "heart_disease": 0,
    "ever_married": "No",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 85.6,
    "bmi": 26.5,
    "smoking_status": "never smoked",
    "stroke": 0,
}

def login(client, email, password):
    client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)


def test_create_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")

    res = client.post("/add-patient", data=sample_patient, follow_redirects=True)
    assert res.status_code == 200
    assert b"New patient record added successfully" in res.data

def test_create_duplicate_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    res = client.post("/add-patient", data=sample_patient, follow_redirects=True)
    assert b"Patient record with this ID already exists." in res.data

def test_update_no_changes_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    res = client.post(f"/update-patient/{sample_patient['id']}", data=sample_patient, follow_redirects=True)
    assert res.status_code == 200
    assert b"No changes made to the patient record." in res.data


def test_update_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    updated_data = sample_patient.copy()
    updated_data["age"] = 50
    res = client.post(f"/update-patient/{sample_patient['id']}", data=updated_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"Patient record updated successfully." in res.data


def test_delete_patient_record_not_admin(client):
    login(client, "doctor@gmail.com", "doctorpass")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    res = client.post(f"/delete-patient/{sample_patient['id']}", follow_redirects=True)
    assert b"Access denied. Only admin can delete patient records." in res.data

def test_delete_patient_record_admin(client):
    login(client, "admin@gmail.com", "asd123asd")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    res = client.post(f"/delete-patient/{sample_patient['id']}", follow_redirects=True)
    assert res.status_code == 200
    assert b"Patient record deleted successfully." in res.data


def test_search_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")
    client.post("/add-patient", data=sample_patient, follow_redirects=True)
    res = client.get(f"/search-patient?search_patient={sample_patient['id']}", follow_redirects=True)
    assert res.status_code == 200

    expected_string = f"Details for patient ID: <b>{sample_patient['id']}</b>".encode('utf-8')
    assert expected_string in res.data

def test_search_nonexistent_patient_record(client):
    login(client, "doctor@gmail.com", "doctorpass")
    res = client.get("/search-patient?search_patient=9999", follow_redirects=True)
    assert b"No Record Found" in res.data