import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA

from mpo.problems.base_problem import MPOBaseProblem
from mpo.utils import RegistersMPOConstruct


@RegistersMPOConstruct(construct_name="problems")
class RastriginFunction(MPOBaseProblem):
    def __init__(self, dim=9):
        self.dim = dim
        super().__init__(
            n_var=dim, n_constr=0, n_obj=1, xu=[5.12] * dim, xl=[-5.12] * dim
        )

    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = -1 * self.func(X)

    def func(self, x):
        A = 10
        return A * self.dim + np.sum(
            x**2 - A * np.cos(2 * np.pi * x), axis=1 if len(x.shape) == 2 else None
        )

    def is_parallelizable(self):
        return True

    def supported_algorithms(self):
        return [GA]
