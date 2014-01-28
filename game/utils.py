import random

from faker import Faker

__all__ = ["PW_LOWER", "PW_UPPER", "PW_NUMBERS", "PW_ALPHA", "PW_ALPHANUM",
           "PW_SYMBOLS", "gen_password", "gen_name"]

PW_LOWER = "abcdefghijklmnopqrstuvwxyz"
PW_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PW_NUMBERS = "1234567890"
PW_ALPHA = PW_LOWER + PW_UPPER
PW_ALPHANUM = PW_ALPHA + PW_NUMBERS
PW_SYMBOLS = "!@#$%^&*()-=_+[]{}\\|;':\",./<>?`~"

def get_port(site):
    """Return the port associated with the given site name."""
    return {
        "qmail": 6680,
        "school": 6673,
        "wife": 6691,
        "bank": 6603
    }[site]

def gen_password(length, chars):
    """Generate a random password of a given length using a certain charset."""
    return "".join([random.choice(chars) for i in xrange(length)])

def gen_name(first=None, last=None):
    """Generate a random name, optionally using a first/last hint."""
    fake = Faker()
    return (first or fake.first_name()) + " " + (last or fake.last_name())
