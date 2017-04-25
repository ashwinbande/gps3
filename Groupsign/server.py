from sympy.ntheory.generate import nextprime, randprime
from sympy.core.numbers import igcdex
from sympy.ntheory import legendre_symbol
from random import randrange


class Server:
    K = 1
    Lp = 32
    LAM2 = 129
    LAM1 = 132
    GAMA2 = 135
    GAMA1 = 138

    P_dash = 4113259823
    P = 8226519647
    Q_dash = 406840943
    Q = 813681887
    N = 6693770029813533889
    N_dash = 1673442505193333089

    A = 4686590024628977158
    A0 = 2209008590724629737
    G = 4025783914985071365

    Y = 4867951024826907980
    X = 351007651139877993

    security_parameters = [K, Lp, LAM1, LAM2, GAMA1, GAMA2]
    public_key = [N, A, A0, Y, G]
    private_key = [P_dash, Q_dash, X]

    def get_security_parameters(self):
        return self.security_parameters

    def get_public_key(self):
        return self.public_key

    def get_alfa_beta(self, Num):
        if legendre_symbol(Num, self.P) == 1 and legendre_symbol(Num, self.Q) == 1:
            ALFAi = randrange(0, 2 ** self.LAM2)
            BETAi = randrange(0, 2 ** self.LAM2)
            return [ALFAi,BETAi]
        else:
            return False, False

    def check_QRn(self, Num):
        if legendre_symbol(Num, self.P) == 1 and legendre_symbol(Num, self.Q) == 1:
            return True
        else:
            return False

    def get_member_cert(self, Num):
        if legendre_symbol(Num, self.P) and legendre_symbol(Num, self.Q) == 1:
            Ei = randprime((2 ** self.GAMA1 - 2 ** self.GAMA2), (2 ** self.GAMA1 + 2 ** self.GAMA2))
            INVE_Ei = igcdex(Ei, ((self.P - 1) * (self.Q - 1)))[0] % ((self.P - 1) * (self.Q - 1))
            Ai = pow((Num * self.A0), INVE_Ei, self.N)
            return [Ai, Ei]
        else:
            return False, False