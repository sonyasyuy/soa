import random
import string


symbols_for_pwd = string.ascii_letters + string.digits


def gen_token() -> str:
    return ''.join([random.choice(symbols_for_pwd) for _ in range(30)])
