def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class",
                          "Basketball", "Tennis Club", "Drama Club",
                          "Digital Art Class", "Debate Team", "Robotics Club"]

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(activities_data) == len(expected_activities)
    assert all(activity in activities_data for activity in expected_activities)


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_info in activities_data.items():
        for field in required_fields:
            assert field in activity_info, f"Missing field '{field}' in {activity_name}"


def test_get_activities_participants_is_list(client):
    """Test that participants field is a list"""
    # Arrange & Act
    response = client.get("/activities")
    activities_data = response.json()

    # Assert
    for activity_name, activity_info in activities_data.items():
        assert isinstance(activity_info["participants"], list), \
            f"Participants should be a list in {activity_name}"
