from urllib.parse import quote

from src.app import activities


def signup_url(activity):
    return f"/activities/{quote(activity)}/signup"


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new@mergington.edu"

    # Act
    response = client.post(signup_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "new@mergington.edu"

    # Act
    response = client.post(signup_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already a participant

    # Act
    response = client.post(signup_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_last_spot_succeeds(client):
    # Arrange
    activity = "Basketball Club"
    limit = activities[activity]["max_participants"]
    activities[activity]["participants"] = [f"s{i}@mergington.edu" for i in range(limit - 1)]
    email = "last@mergington.edu"

    # Act
    response = client.post(signup_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 200
    assert len(activities[activity]["participants"]) == limit


def test_signup_when_full_returns_400(client):
    # Arrange
    activity = "Basketball Club"
    limit = activities[activity]["max_participants"]
    activities[activity]["participants"] = [f"s{i}@mergington.edu" for i in range(limit)]
    email = "late@mergington.edu"

    # Act
    response = client.post(signup_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert len(activities[activity]["participants"]) == limit
    assert email not in activities[activity]["participants"]
