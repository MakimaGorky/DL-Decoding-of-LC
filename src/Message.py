import torch as t
import random as r
from Code import Code
from Noise import Noise


class Message:
    def __init__(self, message=None, is_random=True, length=8):
        # self.encoded_content = None
        # self.modulated_content = None
        # self.decoded_content = None

        if message is not None:
            if t.is_tensor(message):
                self.content = message
            else:
                self.content = t.tensor(message)
            self.length = self.content.size()
            return
        if is_random:
            self.content = Message.__gen_random_message__(length)
            self.length = length
            return

    def __update_content__(self, content):
        if t.is_tensor(content):
            self.content = content
            self.length = content.size()
        else:
            self.content = t.tensor(content)
            self.length = self.content.size()

    def __copy__(self):
        return Message(message=self.content, is_random=False)

    @staticmethod
    def __gen_random_message__(length=8):
        # quite simple randomization
        message = [r.randint(0, 1) for i in range(length)]
        return t.tensor(message)

    def encode(self, encoder=Code()):
        self.__update_content__(encoder.encode(self.content))
        return

    def make_noise(self, noise=Noise()):
        self.__update_content__(self.content + noise.get(self.length[0]))
        return

    def decode(self, decoder=Code()):
        self.__update_content__(decoder.decode(self.content))
