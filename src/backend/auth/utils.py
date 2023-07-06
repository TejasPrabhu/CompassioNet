from werkzeug.security import check_password_hash
from .models import get_user_by_email


def check_invalid_credentials(email, password):
    user = get_user_by_email(email)
    password_match = check_password_hash(user[3], password)

    if not user and (not password_match):
        return True
