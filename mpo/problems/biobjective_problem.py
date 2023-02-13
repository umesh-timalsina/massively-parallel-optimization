import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2

from mpo.problems.base_problem import MPOBaseProblem
from mpo.utils import RegistersMPOConstruct


@RegistersMPOConstruct(construct_name="problems")
class BiObjectiveOptimization(MPOBaseProblem):
    def __init__(self, runner=None, **kwargs):
        self.runner = runner

        super().__init__(
            n_var=2, n_ieq_constr=2, n_obj=2, xu=[2, 2], xl=[-2, -2], **kwargs
        )

    def _evaluate(self, X, out, *args, **kwargs):
        def func1(x):
            return x[0] ** 2 + x[1] ** 2

        def func2(x):
            return (x[0] - 1) ** 2 + x[1] ** 2

        def g1(x):
            return 2 * (x[0] - 0.1) * (x[0] - 0.9) / 0.18

        def g2(x):
            return -20 * (x[0] - 0.4) * (x[0] - 0.6) / 4.8

        if self.runner is None:
            fs = []
            gs = []
            for x in X:
                f1 = func1(x)
                f2 = func2(x)
                c1 = g1(x)
                c2 = g2(x)
                fs.append([f1, f2])
                gs.append([c1, c2])

            out["F"] = np.array(fs)
            out["G"] = np.array(gs)
        else:

            def compute(x):
                return [func1(x), func2(x), g1(x), g2(x)]

            jobs = [self.runner.submit(compute, x) for x in X]

            outs = np.row_stack([job.result() for job in jobs])

            out["F"] = outs[:, :2]
            out["G"] = outs[:, 2:]

    def is_parallelizable(self):
        return True

    def supported_algorithms(self):
        return [NSGA2]

    def post_evaluation(self):
        pass
