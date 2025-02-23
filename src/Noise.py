import torch as t

import random


class Noise:
    def __init__(self):
        return

    @staticmethod
    def get(length):
        strength = 2
        return t.tensor([strength * (2 * random.random() - 1) for i in range(length)])
