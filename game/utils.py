import random

__all__ = ["PW_LOWER", "PW_UPPER", "PW_NUMBERS", "PW_ALPHA", "PW_ALPHANUM",
           "PW_SYMBOLS", "gen_password"]

PW_LOWER = "abcdefghijklmnopqrstuvwxyz"
PW_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PW_NUMBERS = "1234567890"
PW_ALPHA = PW_LOWER + PW_UPPER
PW_ALPHANUM = PW_ALPHA + PW_NUMBERS
PW_SYMBOLS = "!@#$%^&*()-=_+[]{}\\|;':\",./<>?`~"

def gen_password(length, chars):
    """Generate a random password of a given length using a certain charset."""
    return "".join([random.choice(chars) for i in xrange(length)])
