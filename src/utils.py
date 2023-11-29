import random
import string


def generate_string(
    length: int = 16, characters: str = string.ascii_letters + string.digits
):
    return "".join(random.choice(characters) for _ in range(length))