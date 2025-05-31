from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password

def validate_email(email: str) -> bool:
    try:
        validate_email = EmailValidator()
        validate_email(email)
    except:
        return False
    
    return True


def password_validation(password: str) -> bool:
    try:
        validate_password(password)
    except:
        return False
    
    return True
