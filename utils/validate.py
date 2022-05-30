import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex2 = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'


def validate_email(email):
    if re.fullmatch(regex, email):
        return True
    return False


def validate_password(password):
    if re.match(regex2, password):
        return True
    return False
