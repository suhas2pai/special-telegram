def test_signup_successful(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds participant to activity list"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert email in activities_data[activity_name]["participants"]


def test_signup_duplicate_email_fails(client):
    """Test that duplicate signup is rejected"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_different_emails(client):
    """Test multiple students can sign up for the same activity"""
    # Arrange
    activity_name = "Basketball"
    emails = ["student1@mergington.edu", "student2@mergington.edu"]

    # Act multiple signups
    for email in emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    # Assert all are added
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert all(email in participants for email in emails)
