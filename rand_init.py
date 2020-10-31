# generate random integer values
from random import seed as sd
from random import randint

def gen(seed):
    sd(seed)
    while True:
        value = randint(0, 26)
        yield value
