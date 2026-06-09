from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity_name in data
    assert isinstance(data[expected_activity_name]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Science Club"
    participant_email = "newstudent@mergington.edu"
    assert participant_email not in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {participant_email} for {activity_name}"
    }
    assert participant_email in activities[activity_name]["participants"]


def test_signup_for_activity_returns_400_for_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"
    assert participant_email in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_unregisters_student(client):
    # Arrange
    activity_name = "Programming Class"
    participant_email = "emma@mergington.edu"
    assert participant_email in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {participant_email} from {activity_name}"
    }
    assert participant_email not in activities[activity_name]["participants"]


def test_remove_participant_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    participant_email = "nobody@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
