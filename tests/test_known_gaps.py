import pytest


@pytest.mark.xfail(strict=False, reason="API does not enforce max_participants yet")
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    activity_response = client.get("/activities")
    activity = activity_response.json()[activity_name]
    current_count = len(activity["participants"])
    needed_to_fill = activity["max_participants"] - current_count

    for i in range(needed_to_fill):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"fill{i}@mergington.edu"},
        )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


@pytest.mark.xfail(strict=False, reason="API does not validate email format yet")
def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Math Club"
    invalid_email = "not-an-email"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": invalid_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"
