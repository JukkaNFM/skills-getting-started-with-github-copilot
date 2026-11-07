from urllib.parse import quote

from src.app import activities


def remove_url(activity):
    return f"/activities/{quote(activity)}/participants"


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(remove_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in activities[activity]["participants"]


def test_remove_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(remove_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_non_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(remove_url(activity), params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
