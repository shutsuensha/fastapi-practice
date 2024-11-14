async def test_add_booking(authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": 1,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)