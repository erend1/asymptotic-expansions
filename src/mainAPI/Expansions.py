import io
import math
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.mainAPI.Sequences import Sequence


class Expansion:

    def __init__(
            self, sequence: Sequence, x: float, n: int = None
    ):
        self.seq = sequence
        self.x = float(x)
        self.n = n
        self.seq_n0 = int(self.seq.n0)
        self.eval_flag = False
        self.results = list()
        self.error_results = list()
        self._backend_run()

    def _backend_run(self):
        if self.n is not None:
            self.n = int(self.n)
            self._error_analysis(analysis=False)
        else:
            self.n = int(self.x)
            self._error_analysis(analysis=True)
        return self

    def _sum(self, temp_n=None):
        if temp_n is None:
            temp_n = self.n
        total_sum = 0
        self.results = list()
        for index in range(self.seq_n0, temp_n + 1):
            total_sum += self.seq.eval(x=self.x, n=index)
            self.results.append(total_sum)
        self.results.pop()
        return total_sum

    def _error_analysis(self, analysis=True):
        prev_term = abs(self.seq.eval(x=self.x, n=self.seq_n0))
        prev_error = math.inf

        for index in range(self.seq_n0 + 1, self.n + 1):
            next_term = self._sum(temp_n=index)
            next_error = abs(next_term - prev_term)
            self.error_results.append(next_error)
            if analysis:
                if prev_error < next_error:
                    self.n = index
                    break
            prev_term = next_term
            prev_error = next_error
        self.eval_flag = True
        return self

    def get_value(self):
        return self.results[-1]

    def get_all_results(self):

        data_frame = pd.DataFrame(
            {
                "iteration": range(self.seq_n0, len(self.results)),
                "result of expansion": self.results,
                "error between each iteration": self.error_results
            }
        )

        all_results = {
            "data_frame": data_frame,
            "x": self.x,
            "n": self.n,
            "n0": self.seq_n0,
            "results": self.results,
            "errors": self.error_results,
            "iterations": range(self.seq_n0, len(self.results))
        }

        return all_results

    def graph(self, file_name="temp.pdf", path=""):
        n_range = range(self.seq_n0, len(self.results))
        plt.plot(n_range, self.results, 'bx-')
        plt.xlabel('n')
        plt.ylabel('Value of Asymptotic Expansion')
        plt.title('Asymptotic Expansion')
        plt.savefig(path + file_name)
        plt.close()
        return self

    def error_graph(self, file_name="error.pdf", path=""):
        if len(self.error_results) == 0:
            self._error_analysis(analysis=False)
        n_range = range(self.seq_n0, len(self.error_results))
        plt.plot(n_range, self.error_results, 'bx-')
        plt.xlabel('n')
        plt.ylabel('Term Differences')
        plt.title('Asymptotic Expansion Error Analysis')
        plt.savefig(path + file_name)
        plt.close()
        return self


if __name__ == "__main__":
    seq = Sequence()
    expan = Expansion(
        sequence=seq, x=10
    )
    print(
        expan.results
    )
