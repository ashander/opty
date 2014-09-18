import numpy as np
from numpy import testing
import sympy as sp

from utils import ufuncify_matrix


def test_ufuncify_matrix():

    a, b, c = sp.symbols('a, b, c')

    expr_00 = a**2 * sp.cos(b)**c
    expr_01 = sp.tan(b) / sp.sin(a + b) + c**4
    expr_10 = a**2 + b**2 - sp.sqrt(c)
    expr_11 = ((a + b + c) * (a + b)) / a * sp.sin(b)

    sym_mat = sp.Matrix([[expr_00, expr_01],
                         [expr_10, expr_11]])

    # These simply set up some large one dimensional arrays that will be
    # used in the expression evaluation.

    n = 10000

    a_vals = np.random.random(n)
    b_vals = np.random.random(n)
    c_vals = np.random.random(n)
    c_val = np.random.random(1)[0]

    def eval_matrix_loop_numpy(a_vals, b_vals, c_vals):
        """Since the number of matrix elements are typically much smaller
        than the number of evaluations, NumPy can be used to compute each of
        the Matrix expressions. This is equivalent to the individual
        lambdified expressions above."""

        result = np.empty((n, 2, 2))

        result[:, 0, 0] = a_vals**2 * np.cos(b_vals)**c_vals
        result[:, 0, 1] = np.tan(b_vals) / np.sin(a_vals + b_vals) + c_vals**4
        result[:, 1, 0] = a_vals**2 + b_vals**2 - np.sqrt(c_vals)
        result[:, 1, 1] = (((a_vals + b_vals + c_vals) * (a_vals + b_vals))
                           / a_vals * np.sin(b_vals))

        return result

    f = ufuncify_matrix((a, b, c), sym_mat)

    result = np.empty((n, 4))

    testing.assert_allclose(f(result, a_vals, b_vals, c_vals),
                            eval_matrix_loop_numpy(a_vals, b_vals, c_vals))

    f = ufuncify_matrix((a, b, c), sym_mat, const=(c,))

    result = np.empty((n, 4))

    testing.assert_allclose(f(result, a_vals, b_vals, c_val),
                            eval_matrix_loop_numpy(a_vals, b_vals, c_val))