#!/env/bin/py
import re
from urllib.parse import urlparse

def url_validator(value):
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def domain_validator(value):
    pattern = r"^(((?:[*a-zA-Z0-9-.]){2,61}(?:\.[a-zA-Z]{2,})+|(?:[a-zA-Z0-9-]){2,64}))?$"
    try:
        if re.match(pattern, str(value)):
            return True
    except Exception as e:
        print(value)
        print(type(value))
        raise e
    return False

def reverse_domain_validator(value):
    pattern = r"^((\d{1,3}\.){1,4}).*$"
    try:
        if re.match(pattern, str(value)):
            return True
    except Exception as e:
        print(value)
        print(type(value))
        raise e
    return False

def email_validator_rfc5322(value):
    pattern = r"((?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]))"
    try:
        if re.match(pattern, str(value)):
            return True
    except Exception as e:
        print(value)
        print(type(value))
        raise e
    return False