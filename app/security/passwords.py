from argon2 import PasswordHasher, exceptions as argon2_exceptions


_ph = PasswordHasher(time_cost=3, memory_cost=64 * 1024, parallelism=2, hash_len=32)


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(pwhash: str, password: str) -> bool:
    try:
        return _ph.verify(pwhash, password)
    except (argon2_exceptions.VerifyMismatchError, argon2_exceptions.VerificationError):
        return False
    except Exception:
        return False

