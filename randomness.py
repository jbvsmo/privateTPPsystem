import random
import string


def name(size, letters=string.ascii_lowercase):
    return ''.join(random.choice(letters) for _ in range(size))


def select_name(do_not=(), size_random=7):
    names = (
        'Bob', 'Juan', 'Red', 'Blue', 'Oak', 'Mega Mewtwo X',
        'Ray Charles', 'Jesse Pinkman', 'Walter White', 'Pikachu',
        'Gary', 'Ash', 'Suzy', 'Misty', 'Brock', 'Punk', 'Tarzan',
        'Smeagol', 'Ricardão', 'Hodor', 'Joffrey', 'Bruce Wayne',
        'Wolverine', 'Mendigo', 'Capitão Caverna', 'Xuxa',
        'Ted', 'Barney', 'Marshall', 'Lily', 'Robin', 'Batman',
        'Gandalf', 'Frodo', 'Bilbo', 'Smaug', 'Garbodor',
        'ABBBBBBK(', 'Jay Leno', 'Zapdos', 'Helix Fossil',
        'Poochyena', 'Patrick', 'Jennifer Lawrence', 'AJ',
        'Sherlock Holmes', 'Samuel L. Jackson', 'Yo Mama',
    )
    for _ in range(5):
        n = random.choice(names)
        if n not in do_not:
            return n
    return name(size_random)