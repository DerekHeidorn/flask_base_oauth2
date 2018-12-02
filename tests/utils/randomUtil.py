import string
from random import randint
from random import choice


def random_username():
    rand = random_string(3, 20)

    return "USERNAME." + rand + "@tester.com.invali"


def random_string(min_char, max_char):
    all_char = string.ascii_letters + string.digits
    rand = "".join(choice(all_char) for x in range(randint(min_char, max_char)))
    return rand
