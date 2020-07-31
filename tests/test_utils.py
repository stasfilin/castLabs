from src.utils import get_password_hash, verify_password


def test_get_password_hash():
    password = "SUPER_TEST_PASSWORD"

    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) == True
