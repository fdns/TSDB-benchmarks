import random
import string

def generate_random_domain_iterator(length=10, size=300000):
    random.seed(0)
    result = []
    for i in range(size):
        result.append(''.join(random.choice(string.ascii_lowercase) for _ in range(length)) + ".cl")
    while True:
        yield random.choice(result)

def generate_random_ipv4_mask_iterator():
    random.seed(0)
    result = []
    for i in range(256):
        result.append('{}.0.0.0'.format(i))
    while True:
        yield random.choice(result)

def generate_random_size_iterator():
    while True:
        yield random.randint(10, 500)
