import random
import string

with open('data/random_names.txt', 'rb') as file:
    random_names = file.read().decode('utf-8').strip().splitlines()


def name(size, letters=string.ascii_lowercase):
    return ''.join(random.choice(letters) for _ in range(size))


def select_name(do_not=(), size_random=7):
    for _ in range(5):
        n = random.choice(random_names)
        if n not in do_not:
            return n
    return name(size_random)