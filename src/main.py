from Code import *
from Message import *
from Modulator import *
from Noise import *


coder = Code(from_file=True, modulator=BPSK())

print('\tencoding matrix:\n', coder.encoding_matrix)
print('\tsyndrome matrix:\n', coder.syndrome_matrix)

m = Message(length=4, is_random=True)

print('\trandom message:\n', m.content)
m.encode(coder)

print('\tencoded and modulated:\n', m.content)

m.make_noise(Noise())

print('\tnoisy message:\n', m.content)

print('\tf:\n', coder.get_abses(m.content))

print('\t~c:\n', coder.demodulate(m.content))

print('\tS:\n', coder.get_syndrome(m.content))