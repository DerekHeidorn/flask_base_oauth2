import string
from random import randint
from random import choice




def randomUsername():
    rand = randomString(3, 20)

    return "USERNAME." + rand + "@tester.com.invali"

def randomString(min_char, max_char):
    allchar = string.ascii_letters + string.digits
    rand = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return rand

