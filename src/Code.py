import torch as t


class Code:
    ENC_MATR_FN = '../input/G.txt'
    SYN_MATR_FN = '../input/H.txt'

    def __init__(self,
                 encoding_matrix=None,
                 syndrome_matrix=None,
                 from_file=True,
                 encoding_matrix_filename=ENC_MATR_FN,
                 syndrome_matrix_filename=SYN_MATR_FN,
                 modulator=None
                 ):
        if from_file:
            self.encoding_matrix = Code.__parse_matrix__(encoding_matrix_filename)
            self.syndrome_matrix = Code.__parse_matrix__(syndrome_matrix_filename)
        else:
            self.encoding_matrix = encoding_matrix
            self.syndrome_matrix = syndrome_matrix
        self.modulator = modulator
        return

    @staticmethod
    def __parse_matrix__(filename):
        try:
            with open(filename, 'r') as f:
                matr = t.tensor([[int(elem) for elem in line.split()] for line in f.readlines()])
                return matr
        except Exception as e:
            print('bad filename')
            raise

    def modulate(self, encrypted_message):
        return self.modulator.modulate(encrypted_message)

    def encode(self, message):
        encrypted_message = t.matmul(message, self.encoding_matrix) % 2
        if self.modulator is not None:
            encrypted_message = self.modulate(encrypted_message)
        return encrypted_message

    def demodulate(self, encrypted_message):
        return self.modulator.demodulate(encrypted_message)

    def get_syndrome(self, encrypted_message):
        if self.modulator is not None:
            encrypted_message = self.demodulate(encrypted_message)
        return t.matmul(encrypted_message, self.syndrome_matrix.T) % 2

    @staticmethod
    def get_abses(message):
        return t.abs(message)

    def decode(self, encrypted_message):
        return self.get_syndrome(encrypted_message)
