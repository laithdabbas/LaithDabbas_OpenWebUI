from open_webui.services.license_service import (
    check_user_limit,
    validate_license,
    LicenseInvalidError,
    LicenseLimitExceeded,
)


class LicenseError(Exception):
    pass


def check_registration_limit(current_user_count: int):
    try:
        check_user_limit(current_user_count=current_user_count)
    except LicenseLimitExceeded as exc:
        raise LicenseError(str(exc))
    except LicenseInvalidError as exc:
        raise LicenseError(str(exc))


def is_license_valid() -> bool:
    """Check if the license is valid (signature and required fields)."""
    try:
        return validate_license()
    except Exception:
        return False
