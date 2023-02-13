import time

import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA

from mpo.problems.base_problem import MPOBaseProblem
from mpo.utils import RegistersMPOConstruct


@RegistersMPOConstruct(construct_name="problems")
class RastriginFunction(MPOBaseProblem):
    def __init__(self, dim=9, runner=None, **kwargs):
        self.dim = dim
        self.runner = runner

        super().__init__(
            n_var=dim,
            n_constr=0,
            n_obj=1,
            xu=[5.12] * dim,
            xl=[-5.12] * dim,
            **kwargs
        )

    def _evaluate(self, X, out, *args, **kwargs):
        def func(dim, x):
            A = 10
            time.sleep(0.1)
            return A * dim + np.sum(
                x**2 - A * np.cos(2 * np.pi * x),
                axis=1 if len(x.shape) == 2 else None,
            )

        fs = []

        if self.runner is None:
            for x in X:
                f = func(self.dim, x)
                fs.append(f)

            out["F"] = -1 * np.array(fs)
        else:
            jobs = [self.runner.submit(func, self.dim, x) for x in X]
            out["F"] = np.row_stack([job.result() for job in jobs])

    def is_parallelizable(self):
        return True

    def supported_algorithms(self):
        return [GA]

    def post_evaluation(self):
        pass
