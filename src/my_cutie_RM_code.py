import torch as t
from itertools import combinations


class ReedMuller:
    def __init__(self, m, r):
        self.m = m
        self.r = r
        self.message_length = None
        self.encoding_matrix = None
        self.etc = None
        return


def RM_to_files(m, r, encoding_matrix_filename='G.txt', decoding_matrix_filename='H.txt'):
    with open(encoding_matrix_filename, 'w') as enc:
        enc_matr = gen_G(m, r)
        for line in enc_matr:
            enc.write(line)
    with open(decoding_matrix_filename, 'w') as dec:
        dec_matr = gen_H(m, r)
        for line in dec_matr:
            dec.write(line)


def encode(message, m, r):
    if len(message.shape) == 1:
        message = message.unsqueeze(0)
    encoded_message = t.matmul(message, gen_G(m, r)) % 2
    return encoded_message


def decode(enc_message, m, r):
    syndrome = t.matmul(enc_message, gen_H(m, r).T) % 2

    if not t.all(syndrome == 0):
        # TODO correct errors
        return
    # bread
    # decoded_message = enc_message.squeeze(0)[:m + 1]

    # G_pinv = t.pinverse(gen_G(m, r).float())
    # decoded_message = t.matmul(G_pinv, enc_message.float()) % 2
    # decoded_message = decoded_message.int()

    # return decoded_message
    # TODO decode
    deg = gen_G(m, r).size()[0]

    res = []



# like genji
def gen_RM_matrix(m, r):
    n = pow(2, m)
    # g0 generating
    g0 = t.ones(1, n, dtype=t.int)
    if r == 0:
        return g0

    # The G1 generating
    g1 = t.zeros(n, m, dtype=t.int)
    num = 0
    for i in range(n):
        bnum = bin(num)[2:]
        if len(bnum) < m:
            bnum = '0' * (m - len(bnum)) + bnum
        g1[i] = t.tensor([int(d) for d in bnum])
        num += 1
    g1 = t.t(g1)

    # The G like a cat of lil gs
    G = t.cat((g0, g1), dim=0)

    if r < 2:
        return G

    # other Gs
    for i in range(2, r + 1):
        for cmb in combinations(range(m), i):
            cur = t.ones(1, n, dtype= t.int)
            for i in cmb:
                cur = t.bitwise_and(cur, g1[i])
            G = t.cat((G, cur.view(1,n)), dim= 0)

    return G


def gen_RM_matrix_deepseek(m, r):
    # Список всех мономов степени <= r
    monomials = []
    for degree in range(r + 1):
        for vars_comb in combinations(range(m), degree):
            monomials.append(vars_comb)

    # Количество строк в матрице G (число мономов)
    num_rows = len(monomials)
    # Количество столбцов в матрице G (2^m)
    num_cols = 2 ** m

    # Создаём матрицу G
    G = t.zeros((num_rows, num_cols), dtype=t.int)

    # Заполняем матрицу G
    for i, monomial in enumerate(monomials):
        for j in range(num_cols):
            # Преобразуем индекс j в бинарный вектор (значения переменных)
            binary = [int(bit) for bit in f"{j:0{m}b}"]
            # Вычисляем значение монома
            value = 1
            for var in monomial:
                value *= binary[var]
            G[i, j] = value

    return G


def gen_G(m,r):
    return gen_RM_matrix(m, r)


def gen_H(m, r):
    return gen_RM_matrix(m, m - r - 1)


print('test')
G = gen_G(3, 1)
print(G)
#
# G_pinv = t.pinverse(G.float())
# print(G_pinv)
# enc_mes = t.tensor([[1, 0, 0, 1, 0, 1, 1, 0]], dtype= t.int)
# decoded_message = t.matmul(enc_mes.float(), G_pinv) #% 2
# decoded_message = decoded_message.int()
# print(decoded_message)
#
# c = np.array([1, 0, 0, 1, 0, 1, 1, 0])
#
# G_pinv1 = np.linalg.pinv(G)
#
# m = np.dot(c, G_pinv1)
#
# m = np.round(m).astype(int)
#
# print(m)

print(t.matmul(t.tensor([1,1,1,1], dtype=t.int), G) % 2)

H = gen_H(3, 1)
print(H)
print(t.matmul(G, H.T) % 2)
print('test')


message = t.tensor([1, 0, 1, 0], dtype=t.int)

enc_m = encode(message, 3, 1)
print(enc_m)
print()
dec_m = decode(enc_m, 3, 1)
print(dec_m)
