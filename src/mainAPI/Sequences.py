import math


class Sequence:

    def __init__(self, sequence_name: str = None):
        self.seq_dict = {
            "exponential": self._exponential
        }
        if sequence_name in self.seq_dict:
            self.main_seq = self.seq_dict[sequence_name]
        else:
            self.main_seq = self._exponential

        self._status = False
        self.x = None
        self.n = None
        self.n0 = 0
        self.formulas_mat_jax = []

    def _update_values(self, x, n):
        try:
            self.x = float(x)
            self.n = int(n)
            self._status = True
        except ValueError:
            print(f"Given x and n could not converted into float and integer: {self.x}, {self.n}")
            self._status = False
        return self

    def eval(self, x: float, n: int):
        self._update_values(x=x, n=n)
        if not self._status:
            return None
        return self.main_seq()

    def _exponential(self):
        self.n0 = 0
        self.formulas_mat_jax = [
            r"\text{Ei}",
            r"\[ \text{Ei}( x ) = \int \limits _ x ^{\infty} \dfrac{e^{-t}}{t} \text{d}t, \qquad x >0. \]",
            r"\[ \text{Ei}( x ) \sim e^{- x } \sum_{ k = 0 }^{ n - 1 } (-1)^{ k } \dfrac{ k !}{x^{ k + 1}}, "
            r"\quad \text{ as } x \to \infty .\]",
        ]
        result = ((-1) ** self.n) * (math.exp(-self.x)) * (math.factorial(self.n) / self.x ** (self.n + 1))
        return result
