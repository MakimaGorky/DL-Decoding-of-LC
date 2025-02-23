import torch as t


class BPSK:
    def __init__(self):
        return

    @staticmethod
    def modulate(message):
        # return t.tensor([-1 if elem == 0 else 1 for elem in message.data])
        return t.where(message == 1, t.tensor(1), t.tensor(-1))

    @staticmethod
    def demodulate(message):
        return t.where(message > 0, t.tensor(1), t.tensor(0))