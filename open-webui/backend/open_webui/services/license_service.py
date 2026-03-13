import base64
import json
import logging
from pathlib import Path
from typing import Any, Optional

from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["CONFIG"])

LICENSE_FILE_PATH = Path(__file__).resolve().parent.parent / "license.json"

# Replace this key in production with your own RSA public key.
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz51RS4kyc2aFDLvT4HIs
PRK+rrNbuIDhhCoiuQ6C0n3/6M9sCdNhtrmbJP4M62IDyabpXJ9yiBZdOwEdtjsq
YZIGmURh98Q6z4Y0magymVsbLnqhcHXyXwmlpfvIsUOxy4ptMGCOsh7Wzd36Sp4D
HaS0dvdSX6Ok3sh1vQaLvUOFswSK/K6IjhqCwSz77njNSAnWpqwvCv5e/itESpcj
q/4M4bR1bayy6t9K//faOf23kfhMZK7UI1zVO0DRyCX45d0hlHfy47PL7dex/DUB
n1nOWnEKZzJcNnbkSusrPU4cSLZPYfjB9q4S31J0yBQVleQVO+45F8A5T5/N2PKg
QQIDAQAB
-----END PUBLIC KEY-----"""

_LICENSE_CACHE: Optional[dict[str, Any]] = None
_LICENSE_VALID: Optional[bool] = None
_LICENSE_MAX_USERS: Optional[int] = None


class LicenseError(Exception):
    pass


class LicenseInvalidError(LicenseError):
    pass


class LicenseLimitExceeded(LicenseError):
    pass


def _canonical_payload(license_data: dict[str, Any]) -> bytes:
    payload = {k: v for k, v in license_data.items() if k != "signature"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _load_public_key():
    try:
        from cryptography.hazmat.primitives import serialization
    except Exception as exc:
        log.error(f"License: cryptography not available: {exc}")
        return None

    try:
        return serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode("utf-8"))
    except Exception as exc:
        log.error(f"License: failed to load public key: {exc}")
        return None


def _validate_license_data(license_data: dict[str, Any]) -> bool:
    try:
        licensee = license_data.get("licensee")
        max_users = license_data.get("max_users")
        signature_b64 = license_data.get("signature")

        if not isinstance(licensee, str) or not licensee.strip():
            return False
        if not isinstance(max_users, int) or max_users <= 0:
            return False
        if not isinstance(signature_b64, str) or not signature_b64.strip():
            return False

        public_key = _load_public_key()
        if public_key is None:
            return False

        payload = _canonical_payload(license_data)
        signature = base64.b64decode(signature_b64)

        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding

        public_key.verify(signature, payload, padding.PKCS1v15(), hashes.SHA256())
        return True
    except Exception as exc:
        log.error(f"License: validation failed: {exc}")
        return False


def load_license(force_reload: bool = False) -> dict[str, Any]:
    global _LICENSE_CACHE, _LICENSE_VALID, _LICENSE_MAX_USERS

    if _LICENSE_CACHE is not None and not force_reload:
        return _LICENSE_CACHE

    if not LICENSE_FILE_PATH.exists():
        log.warning(f"License file not found: {LICENSE_FILE_PATH}")
        _LICENSE_CACHE = {}
        _LICENSE_VALID = False
        _LICENSE_MAX_USERS = None
        return _LICENSE_CACHE

    try:
        _LICENSE_CACHE = json.loads(LICENSE_FILE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        log.error(f"License: failed to read license file: {exc}")
        _LICENSE_CACHE = {}

    _LICENSE_VALID = _validate_license_data(_LICENSE_CACHE)

    if _LICENSE_VALID:
        _LICENSE_MAX_USERS = int(_LICENSE_CACHE.get("max_users"))
    else:
        _LICENSE_MAX_USERS = None

    return _LICENSE_CACHE


def validate_license(license_data: Optional[dict[str, Any]] = None) -> bool:
    global _LICENSE_VALID

    if license_data is None:
        if _LICENSE_VALID is None:
            load_license()
        return bool(_LICENSE_VALID)

    return _validate_license_data(license_data)


def get_max_users() -> int:
    if _LICENSE_VALID is None:
        load_license()

    if not _LICENSE_VALID or _LICENSE_MAX_USERS is None:
        raise LicenseInvalidError("License is invalid or missing.")

    return _LICENSE_MAX_USERS


def check_user_limit(current_user_count: Optional[int] = None) -> None:
    max_users = get_max_users()

    if current_user_count is None:
        # Import here to avoid circular imports
        from open_webui.models.users import Users

        current_user_count = Users.get_num_users() or 0

    if current_user_count >= max_users:
        raise LicenseLimitExceeded(f"License user limit reached ({max_users}).")
