import random
def generate_numeric_code(length: int) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))