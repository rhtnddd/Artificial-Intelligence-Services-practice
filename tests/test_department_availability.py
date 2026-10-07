import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "department,equipment_id,quantity,available,expected",
    [
        ("it", 1, 3, 3, True),
        ("general", 1, 3, 3, False),
        ("general", 1, 2, 3, True),
        ("it", 1, 4, 3, False),
        ("general", 2, 1, 0, False),
        (None, 1, 3, 3, True),
    ],
)
def test_department_availability(department, equipment_id, quantity, available, expected):
    params = {"quantity": quantity}
    if department is not None:
        params["department"] = department
    response = client.get(f"/equipment/{equipment_id}/availability", params=params)
    assert response.status_code == 200
    assert response.json() == {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": expected,
    }


@pytest.mark.parametrize(
    "department,quantity",
    [("sales", 1), ("IT", 1), ("it", 0)],
)
def test_invalid_input_is_rejected(department, quantity):
    response = client.get(
        "/equipment/1/availability",
        params={"department": department, "quantity": quantity},
    )
    assert response.status_code == 422


def test_unknown_equipment_returns_404():
    response = client.get(
        "/equipment/99/availability", params={"department": "general", "quantity": 1}
    )
    assert response.status_code == 404
