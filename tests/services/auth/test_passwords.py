from deeptutor.services.auth.passwords import hash_password, verify_password


def test_hash_and_verify_password_roundtrip() -> None:
    hashed = hash_password("StrongPass123!")
    assert hashed != "StrongPass123!"
    assert verify_password("StrongPass123!", hashed) is True
    assert verify_password("WrongPass123!", hashed) is False
