import io
import math
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Sequence:

    @staticmethod
    def exponential(x, n):
        """

        :param float x:
        :param int n:
        :return:
        """
        result = ((-1)**n) * (math.exp(-x)) * (math.factorial(n)/x**(n+1))
        return result


class Expansion:

    def __init__(self, sequence, x, n=None, sequence_start_index=0):
        """

        :param sequence:
        :param float x:
        :param int n:
        :param int sequence_start_index:
        """

        self.sequence = sequence
        self.x = float(x)
        self.int_x = int(x)
        self.n = n
        self.sequence_start_index = int(sequence_start_index)
        self.eval_flag = False
        self.results = list()
        self.error_results = list()
        self._check_n()
        self.eval()

    def _check_n(self):
        if self.n is None:
            self.n = self.int_x
            self._error_analysis()
        return self

    def _sum(self, temp_n=None):
        if temp_n is None:
            temp_n = self.n
        total_sum = 0
        self.results = list()
        for index in range(self.sequence_start_index, temp_n+1):
            total_sum += self.sequence(x=self.x, n=index)
            self.results.append(total_sum)
        self.results.pop()
        return total_sum

    def _error_analysis(self, analysis=True):
        prev_term = abs(self.sequence(x=self.x, n=self.sequence_start_index))
        prev_error = math.inf

        for index in range(self.sequence_start_index+1, self.n+1):
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

    def eval(self):
        if self.eval_flag:
            return self.results[-1]
        else:
            return self._sum()

    def graph(self, file_name="temp.pdf", path=""):
        n_range = range(self.sequence_start_index, len(self.results))
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
        n_range = range(self.sequence_start_index, len(self.error_results))
        plt.plot(n_range, self.error_results, 'bx-')
        plt.xlabel('n')
        plt.ylabel('Term Differences')
        plt.title('Asymptotic Expansion Error Analysis')
        plt.savefig(path + file_name)
        plt.close()
        return self


if __name__ == "__main__":

    def main():
        import matplotlib
        from matplotlib import pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages

        #plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True

        X = [1000]

        seq = Sequence.exponential

        for item in X:
            temp_expns = Expansion(
                sequence=seq, x=item
            )

            plt.figure()
            temp_result = temp_expns.results
            plt.plot(
                range(0, len(temp_result)),
                temp_result
            )
            plt.xlabel('n')
            plt.ylabel('Term Differences')
            plt.title(f"x = {item}")
            print(f"--------------{item}-----------")
            print(temp_expns.n)
            print(temp_expns.eval())
            try:
                print((temp_expns.results[-1] - temp_expns.results[-2]) / (temp_expns.results[-3] - temp_expns.results[-4]))
            except ZeroDivisionError:
                pass
            # PdfPages is a wrapper around pdf
            # file so there is no clash and create
            # files with no error.
            p = PdfPages("test.pdf")

            # get_fignums Return list of existing
            # figure numbers
            fig_nums = plt.get_fignums()
            figs = [plt.figure(n) for n in fig_nums]

            # iterating over the numbers in list
            for fig in figs:
                # and saving the files
                fig.savefig(p, format='pdf')

            # close the object
            p.close()

    main()
