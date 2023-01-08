import numpy as np
import galois as gs


class Crypto:
    def __init__(self, language: str = "tr"):
        self.abc = {}
        self._generate_abc(language)
        self.inv_abc = {v: k for k, v in self.abc.items()}
        self.norm = len(self.abc)
        self.gs = gs.GF(self.norm)

        self.word = None
        self.word_norm = None
        self.word_arr = None
        self.lock = None
        self.constant = None
        self.key = None
        self.encrypted = None
        self.word_encrypted = None

    def _status(self):
        condition = bool(
             self.lock is None or self.key is None
        )
        return not condition

    def _print(self, encryption: bool = True):
        if encryption:
            first_str = "Encrypted"
            second_str = "Decrypted"
        else:
            first_str = "Decrypted"
            second_str = "Encrypted"

        print("--------Formula--------")
        print("Ax + b = y,")
        print("x = inv(A)*(y - b),")
        print("where x: decrypted, y: encrypted word, \n"
              "A: lock, inv(A): key, b: constant")
        print(f"-------{second_str} Word---------")
        print(self.word)
        print(f"-------{first_str} Word---------")
        print(self.word_encrypted)
        print("--------Lock---------")
        print(self.lock)
        print("--------Key----------")
        print(self.key)
        print("-------Constant-------")
        print(self.constant)
        print(f"---------Array of {second_str} Word-------")
        print(self.word_arr)
        print(f"---------Array of {first_str} Word-------")
        print(self.encrypted)

    def get_all_params(self):
        all_params = {
            "word": str(self.word),
            "word_norm": int(self.word_norm),
            "word_arr": np.array(self.word_arr).tolist(),
            "lock": np.array(self.lock).tolist(),
            "constant": np.array(self.constant).tolist(),
            "key": np.array(self.key).tolist(),
            "transformed_arr": np.array(self.encrypted).tolist(),
            "word_transformed": str(self.word_encrypted)
        }
        return all_params

    def _generate_abc(self, language):
        if language is None:
            language = "tr"
        language = str(language).strip().lower()
        if language == "tr":
            self.abc = {
                "a": 1,
                "b": 2,
                "c": 3,
                "ç": 4,
                "d": 5,
                "e": 6,
                "f": 7,
                "g": 8,
                "ğ": 9,
                "h": 10,
                "ı": 11,
                "i": 12,
                "j": 13,
                "k": 14,
                "l": 15,
                "m": 16,
                "n": 17,
                "o": 18,
                "ö": 19,
                "p": 20,
                "r": 21,
                "s": 22,
                "ş": 23,
                "t": 24,
                "u": 25,
                "ü": 26,
                "v": 27,
                "y": 28,
                "z": 0
            }
        elif language == "eng":
            self.abc = {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
                "e": 5,
                "f": 6,
                "g": 7,
                "h": 8,
                "i": 9,
                "j": 10,
                "k": 11,
                "l": 12,
                "m": 13,
                "n": 14,
                "o": 15,
                "p": 16,
                "q": 17,
                "r": 18,
                "s": 19,
                "t": 20,
                "u": 21,
                "v": 22,
                "w": 23,
                "x": 24,
                "y": 25,
                "z": 26,
                ".": 27,
                ",": 28,
                "!": 0
            }

    def _generate_word_arr(self):
        self.word_arr = []
        for char in self.word:
            try:
                self.word_arr.append(self.abc[char])
            except KeyError:
                print(f"The char could not be found in the alphabet: {char}")
                self.word_arr.append(1)
        self.word_arr = self.gs(np.array(self.word_arr))
        return self

    def _generate_word(self):
        if self.encrypted is None:
            return self
        word = str()
        for key in self.encrypted:
            word += self.inv_abc[int(key)]
        return word

    def _generate_constant(self, constant: np.ndarray):
        if constant is None:
            self.constant = self.gs(np.zeros(self.word_norm, dtype=int))
        else:
            self.constant = self.gs(constant)
        return self

    def generate_cipher(self, cipher: np.ndarray = None):
        if len(self.word) >= 29:
            print("It is not recommended to use this crypto technique for a word that has more than 29 characters.")
            self.word_norm = len(self.abc)
        else:
            self.word_norm = len(self.word)

        if cipher is not None:
            self.lock = self.gs(cipher)
        else:
            self.lock = self.gs.Random((self.word_norm, self.word_norm))

        while np.linalg.matrix_rank(self.lock) < self.word_norm:
            print("Defined cipher does not have inverse. So, the cipher will be re-defined.")
            self.lock = self.gs.Random((self.word_norm, self.word_norm))

        self.key = self.gs(np.linalg.inv(self.lock))
        return self

    def encryption(self, word: str, cipher: np.ndarray = None, constant: np.ndarray = None):
        self.word = str(word)
        self.word_norm = len(word)
        if cipher is not None:
            self.generate_cipher(cipher=cipher)
        if not self._status():
            self.generate_cipher()
        self._generate_word_arr()
        self._generate_constant(constant=constant)
        self.encrypted = self.gs(np.matmul(self.lock, self.word_arr)) + self.constant
        self.word_encrypted = self._generate_word()
        self._print()
        return self.word_encrypted

    def decryption(self, word: str, cipher: np.ndarray = None, constant: np.ndarray = None):
        self.word = str(word)
        self.word_norm = len(word)
        if cipher is not None:
            self.generate_cipher(cipher=cipher)
        if not self._status():
            return None
        self._generate_word_arr()
        self._generate_constant(constant=constant)
        self.encrypted = np.matmul(self.key, self.gs((self.word_arr - self.constant)))
        self.word_encrypted = self._generate_word()
        self._print(encryption=False)
        return self.word_encrypted


class Ciphers(Crypto):
    def __init__(self, word: str):
        super().__init__()
        self.word = str(word)
        self.word_norm = len(self.word)
        self.A = self.gs(np.identity(n=self.word_norm, dtype=int))
        self.b = self.gs(np.zeros(self.word_norm, dtype=int))

        self.ciphers_dict = {
            "caesar": self.caesar,
            "example1": self.example1,
            "example2": self.example2,

        }

    def get(self, key: str):
        try:
            the_function = self.ciphers_dict[key]
        except KeyError:
            return None, None
        return the_function()

    def caesar(self):
        self.A = self.gs(np.identity(n=self.word_norm, dtype=int))
        self.b = 3 * self.gs(np.ones(self.word_norm, dtype=int))
        return self.A, self.b

    def example1(self):
        self.A = 3 * self.gs(np.identity(n=self.word_norm, dtype=int))
        self.b = -4 * self.gs(np.ones(self.word_norm, dtype=int))
        return self.A, self.b

    def example2(self):
        inverse_3 = self.gs([1]) / self.gs([3])
        self.A = self.gs(np.identity(n=self.word_norm, dtype=int)) * inverse_3[0]
        self.b = self.gs(np.ones(self.word_norm, dtype=int)) * inverse_3[0]
        return self.A, self.b


if __name__ == "__main__":
    Cr = Crypto(language="tr")
    word_1 = "dçelooyu"
    word_2 = "yohüaydcç"
    word_3 = "apdoinkv"

    word_1_A, word_1_b = Ciphers(word=word_1).caesar()
    word_2_A, word_2_b = Ciphers(word=word_2).example1()
    word_3_A, word_3_b = Ciphers(word=word_3).example2()

    Cr.decryption(word_1, word_1_A, word_1_b)
    Cr.decryption(word_2, word_2_A, word_2_b)
    Cr.decryption(word_3, word_3_A, word_3_b)
