import random
import string


def generate_string(length=16, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))