from collections.abc import Generator
from uuid import UUID

import pytest
from app.main import app
from app.security.jwt import create_access_token
from app.users.user_model import UserModel
from database.base import Base
from database.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

TEST_USER_ID = UUID("abcdefab-cdef-abcd-efab-cdefabcdefab")


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    with testing_session() as db:
        db.add(
            UserModel(
                id=TEST_USER_ID,
                email="test@example.com",
                password_hash="not-used-by-this-test",
            )
        )
        db.commit()

    def override_get_db() -> Generator[Session, None, None]:
        with testing_session() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def authorization_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {create_access_token(TEST_USER_ID)}"
    }


def create_notification(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "Integration test",
            "content": "Notification content",
            "channel": "email",
            "recipient": "recipient@example.com",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_notification_returns_created_notification(
    client: TestClient,
) -> None:
    notification = create_notification(client)

    assert UUID(notification["id"])
    assert notification["user_id"] == str(TEST_USER_ID)
    assert notification["title"] == "Integration test"
    assert notification["content"] == "Notification content"
    assert notification["channel"] == "email"
    assert notification["recipient"] == "recipient@example.com"
    assert notification["created_at"]
    assert notification["updated_at"]


def test_list_notifications_returns_current_users_notifications(
    client: TestClient,
) -> None:
    notification = create_notification(client)

    response = client.get(
        "/notifications",
        headers=authorization_headers(),
    )

    assert response.status_code == 200
    assert response.json() == [notification]


def test_get_notification_by_id_returns_notification(
    client: TestClient,
) -> None:
    notification = create_notification(client)

    response = client.get(
        f"/notifications/{notification['id']}",
        headers=authorization_headers(),
    )

    assert response.status_code == 200
    assert response.json() == notification


def test_update_notification_returns_updated_notification(
    client: TestClient,
) -> None:
    notification = create_notification(client)
    response = client.put(
        f"/notifications/{notification['id']}",
        headers=authorization_headers(),
        json={
            "title": "Updated title",
            "content": "Updated content",
            "channel": "email",
            "recipient": "updated@example.com",
        },
    )

    assert response.status_code == 200
    updated_notification = response.json()
    assert updated_notification["id"] == notification["id"]
    assert updated_notification["user_id"] == str(TEST_USER_ID)
    assert updated_notification["title"] == "Updated title"
    assert updated_notification["content"] == "Updated content"
    assert updated_notification["channel"] == "email"
    assert updated_notification["recipient"] == "updated@example.com"
    assert updated_notification["created_at"] == notification["created_at"]
    assert updated_notification["updated_at"]


def test_delete_notification_removes_it_from_user_list(
    client: TestClient,
) -> None:
    notification = create_notification(client)
    response = client.delete(
        f"/notifications/{notification['id']}",
        headers=authorization_headers(),
    )

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(
        "/notifications",
        headers=authorization_headers(),
    ).json() == []


def test_create_notification_rejects_invalid_email_recipient(
    client: TestClient,
) -> None:
    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "Integration test",
            "content": "Notification content",
            "channel": "email",
            "recipient": "not-an-email",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email recipient"}


def test_create_notification_rejects_oversized_sms_without_saving(
    client: TestClient,
) -> None:
    from core.config import settings

    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "Integration test",
            "content": "x" * (settings.sms_max_length + 1),
            "channel": "sms",
            "recipient": "+12345678901",
        },
    )

    assert response.status_code == 400
    assert client.get(
        "/notifications",
        headers=authorization_headers(),
    ).json() == []


def test_update_notification_rejects_oversized_sms_without_updating(
    client: TestClient,
) -> None:
    from core.config import settings

    notification = create_notification(client)
    response = client.put(
        f"/notifications/{notification['id']}",
        headers=authorization_headers(),
        json={
            "title": "Updated title",
            "content": "x" * (settings.sms_max_length + 1),
            "channel": "sms",
            "recipient": "+12345678901",
        },
    )

    assert response.status_code == 400
    assert client.get(
        f"/notifications/{notification['id']}",
        headers=authorization_headers(),
    ).json() == notification


def test_list_notifications_requires_authentication(
    client: TestClient,
) -> None:
    response = client.get("/notifications")

    assert response.status_code == 401


def test_list_users_returns_all_users(client: TestClient) -> None:
    response = client.get("/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["id"] == str(TEST_USER_ID)
    assert users[0]["email"] == "test@example.com"
    assert users[0]["created_at"]


def test_get_user_by_id_returns_user(client: TestClient) -> None:
    response = client.get(f"/users/{TEST_USER_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == str(TEST_USER_ID)
    assert response.json()["email"] == "test@example.com"


def test_get_user_by_email_returns_not_found_for_unknown_email(
    client: TestClient,
) -> None:
    response = client.get("/users/by-email/missing@example.com")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_my_profile_returns_authenticated_user(
    client: TestClient,
) -> None:
    response = client.get(
        "/users/me",
        headers=authorization_headers(),
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(TEST_USER_ID)
    assert response.json()["email"] == "test@example.com"


def test_register_user_returns_created_user(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "email": "new-user@example.com",
            "password": "SecurePass1!",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new-user@example.com"
    assert response.json()["id"]
    assert response.json()["created_at"]
    assert "password_hash" not in response.json()


def test_register_user_rejects_duplicate_email(
    client: TestClient,
) -> None:
    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "SecurePass1!",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_register_user_rejects_short_password(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "email": "new-user@example.com",
            "password": "Short1!",
        },
    )

    assert response.status_code == 422


def test_login_returns_access_token_for_registered_user(
    client: TestClient,
) -> None:
    client.post(
        "/users",
        json={
            "email": "login@example.com",
            "password": "SecurePass1!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "SecurePass1!",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


def test_login_rejects_unknown_email(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "SecurePass1!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


def test_login_rejects_incorrect_password(client: TestClient) -> None:
    client.post(
        "/users",
        json={
            "email": "login@example.com",
            "password": "SecurePass1!",
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "WrongPass1!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_notification_operations_return_not_found_for_unknown_id(
    client: TestClient,
    method: str,
) -> None:
    notification_id = "12345678-1234-5678-1234-567812345678"
    path = f"/notifications/{notification_id}"
    if method == "get":
        response = client.get(path, headers=authorization_headers())
    elif method == "put":
        response = client.put(
            path,
            headers=authorization_headers(),
            json={
                "title": "Updated title",
                "content": "Updated content",
                "channel": "email",
                "recipient": "recipient@example.com",
            },
        )
    else:
        response = client.delete(path, headers=authorization_headers())

    assert response.status_code == 404
    assert response.json() == {"detail": "Notification not found"}


def test_create_push_notification_returns_created_notification(
    client: TestClient,
) -> None:
    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "Push test",
            "content": "Push content",
            "channel": "push",
            "recipient": "device-token",
        },
    )

    assert response.status_code == 201
    assert response.json()["channel"] == "push"
    assert response.json()["recipient"] == "device-token"


def test_create_push_notification_rejects_empty_recipient(
    client: TestClient,
) -> None:
    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "Push test",
            "content": "Push content",
            "channel": "push",
            "recipient": "   ",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid push recipient"}


def test_create_sms_notification_rejects_invalid_phone_number(
    client: TestClient,
) -> None:
    response = client.post(
        "/notifications",
        headers=authorization_headers(),
        json={
            "title": "SMS test",
            "content": "SMS content",
            "channel": "sms",
            "recipient": "not-a-phone-number",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid SMS recipient"}