from werkzeug.security import check_password_hash, generate_password_hash
from .models import get_user_by_email


def check_invalid_credentials(email, password):
    user = get_user_by_email(email)
    if not user:
        return True
    password_match = check_password_hash(user[3], password)
    return not password_match
