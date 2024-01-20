import random

strings = ["".join(random.choices("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890".split(""),k=20)) for i in range(100000)]
data = [{"string":i} for i in strings]

