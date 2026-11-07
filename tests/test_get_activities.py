from urllib.parse import quote

from src.app import MAX_PARTICIPANTS, activities


def test_get_activities_returns_all(client):
    # Arrange
    expected_names = set(activities)
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data) == expected_names
    for details in data.values():
        assert expected_keys <= set(details)


def test_activities_have_max_100(client):
    # Arrange
    expected_max = 100

    # Act
    response = client.get("/activities")

    # Assert
    assert MAX_PARTICIPANTS == expected_max
    assert all(d["max_participants"] == expected_max for d in response.json().values())


def test_signed_up_participant_is_listed(client):
    # Arrange
    activity = "Art Club"
    email = "listed@mergington.edu"
    client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Act
    response = client.get("/activities")

    # Assert
    assert email in response.json()[activity]["participants"]


def test_removed_participant_is_not_listed(client):
    # Arrange
    activity = "Art Club"
    email = "removed@mergington.edu"
    path = f"/activities/{quote(activity)}"
    client.post(f"{path}/signup", params={"email": email})
    client.delete(f"{path}/participants", params={"email": email})

    # Act
    response = client.get("/activities")

    # Assert
    assert email not in response.json()[activity]["participants"]
