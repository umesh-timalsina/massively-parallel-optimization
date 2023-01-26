import abc

from pymoo.core.problem import ElementwiseProblem


class MPOBaseProblem(ElementwiseProblem):
    def __init__(self, **kwargs):  # Only use keyword arguments
        super().__init__(**kwargs)

    @abc.abstractmethod
    def _evaluate(self, x, out, *args, **kwargs):
        return NotImplemented

    @property
    def supported_algorithms(self):
        return []

    @abc.abstractmethod
    def is_parallelizable(self):
        return NotImplemented
