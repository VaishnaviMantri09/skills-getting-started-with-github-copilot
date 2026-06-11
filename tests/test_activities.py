import urllib.parse

def test_get_activities(client):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    # Arrange
    activity = "Science Club"
    email = "newstudent@mergington.edu"
    encoded = urllib.parse.quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in resp.json().get("message", "")
    get_r = client.get("/activities")
    assert email in get_r.json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Science Club"
    existing_email = "mia@mergington.edu"
    encoded = urllib.parse.quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": existing_email})

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    encoded = urllib.parse.quote(activity, safe="")

    # Act
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded = urllib.parse.quote(activity, safe="")

    # Act
    resp = client.delete(f"/activities/{encoded}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    get_r = client.get("/activities")
    assert email not in get_r.json()[activity]["participants"]


def test_remove_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    missing_email = "nobody@mergington.edu"
    encoded = urllib.parse.quote(activity, safe="")

    # Act
    resp = client.delete(f"/activities/{encoded}/participants", params={"email": missing_email})

    # Assert
    assert resp.status_code == 404
