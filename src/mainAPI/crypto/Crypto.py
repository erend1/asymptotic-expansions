import json
import random
import numpy as np
import galois as gs
import array_to_latex as a2l
from src.utils.Utils import save_key_file_path


class ABC:
    def __init__(self, language: str = None):
        self.abc = {}
        self._generate_abc(language)
        self.inv_abc = {v: k for k, v in self.abc.items()}

    def _generate_abc(self, language):
        if language is None:
            language = "eng"
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
                "z": 29,
                "_": 30,
                ".": 0
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
                "!": 29,
                "_": 30,
                "-": 0
            }


class Crypto(ABC):
    def __init__(self, language: str = None):
        super().__init__(language=language)
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

    def _update_word(self, new_word: str):
        try:
            new_word = str(new_word).strip().lower()
            self.word = new_word
            if len(self.word) >= len(self.abc):
                print("It is not recommended to use this crypto "
                      "technique for a word that has more than total "
                      "number of characters in the alphabet.")
                print("Hence, the remaining part of the word will be"
                      "chopped.")
                self.word = self.word[0:len(self.abc)]
            self.word_norm = len(self.word)

        except Exception as err:
            print(err)
            return self

    def _generate_word_arr(self):
        self.word_arr = []
        for char in self.word:
            try:
                self.word_arr.append(self.abc[char])
            except KeyError:
                temp_char = random.randint(0, len(self.abc))
                self.word_arr.append(temp_char)
                print(
                    f"The char could not be found in the alphabet: {char}.",
                    f"Hence, instead new char has been chosen: {self.abc[temp_char]}."
                )
        self.word_arr = self.gs(np.array(self.word_arr))
        return self

    def _re_generate_word(self):
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

    def _generate_cipher(self, cipher: np.ndarray):
        self.lock = self.gs(cipher)
        self.key = self.gs(np.linalg.inv(self.lock))
        return self

    def encryption(self, word: str, cipher: np.ndarray, constant: np.ndarray):
        self._update_word(new_word=word)
        self._generate_cipher(cipher=cipher)
        self._generate_word_arr()
        self._generate_constant(constant=constant)
        self.encrypted = self.gs(np.matmul(self.lock, self.word_arr)) + self.constant
        self.word_encrypted = self._re_generate_word()
        return self.word_encrypted

    def decryption(self, word: str, cipher: np.ndarray, constant: np.ndarray):
        self._update_word(new_word=word)
        self._generate_cipher(cipher=cipher)
        self._generate_word_arr()
        self._generate_constant(constant=constant)
        self.encrypted = np.matmul(self.key, self.gs((self.word_arr - self.constant)))
        self.word_encrypted = self._re_generate_word()
        return self.word_encrypted

    def save_lock_constant(self, file_name: str = None):
        if file_name is None:
            file_name = "temp"
        content = {
            "A": np.array(self.lock),
            "b": np.array(self.constant)
        }
        save_key_file_path(file_name=file_name, content=content)
        return self

    def get_all_arrays_in_latex(self):
        arrays_in_latex = {
            "word_arr": a2l.to_ltx(np.array(self.word_arr), print_out=False),
            "lock": a2l.to_ltx(np.array(self.lock), print_out=False),
            "constant": a2l.to_ltx(np.array(self.constant), print_out=False),
            "key": a2l.to_ltx(np.array(self.key), print_out=False),
            "encrypted": a2l.to_ltx(np.array(self.encrypted), print_out=False)
        }
        return arrays_in_latex

    def get_all_arrays_in_list(self):
        all_params = {
            "word_arr": np.array(self.word_arr).tolist(),
            "lock": np.array(self.lock).tolist(),
            "constant": np.array(self.constant).tolist(),
            "key": np.array(self.key).tolist(),
            "encrypted": np.array(self.encrypted).tolist(),
        }
        return all_params


class Ciphers(ABC):
    def __init__(self, word: str, language: str = None):
        super().__init__(language=language)
        self.word = str(word)
        self.word_norm = len(self.word)
        self.norm = len(self.abc)
        self.gs = gs.GF(self.norm)
        self.A = self.gs(np.identity(n=self.word_norm, dtype=int))
        self.b = self.gs(np.zeros(self.word_norm, dtype=int))

        self.ciphers_dict = {
            "random": self.random,
            "caesar": self.caesar,
            "example1": self.example1,
            "example2": self.example2,
        }

    def get(self, key: str):
        try:
            self.ciphers_dict[key]()
        except KeyError:
            print("Given method does not exists.")
        return self.A, self.b

    def random(self):
        self.A = self.gs.Random((self.word_norm, self.word_norm))
        while np.linalg.matrix_rank(self.A) < self.word_norm:
            print("Defined cipher does not have inverse. So, the cipher will be re-defined.")
            self.A = self.gs.Random((self.word_norm, self.word_norm))
        self.b = self.gs.Random(self.word_norm)
        return self.A, self.b

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
