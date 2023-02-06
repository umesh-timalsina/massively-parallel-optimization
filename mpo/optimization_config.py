from typing import Any, ClassVar, Dict, Type, Tuple, Union

from pydantic import BaseModel, Field
from pathlib import Path
from mpo.problems.base_problem import MPOBaseProblem
from pymoo.core.algorithm import Algorithm
from pymoo.core.termination import Termination

from datetime import datetime


class OptimizationConfig(BaseModel):
    problems: ClassVar[Dict[str, Any]] = {}

    algorithms: ClassVar[Dict[str, Any]] = {}

    problem: str = Field(
        ...,
        description="The name of the problem to solve",
    )

    algorithm: str = Field(
        ...,
        description="The name of the algorithm on which this problem needs to be solved"
    )

    problem_kwargs: Dict[str, Any] = Field(
        default={}, description="The key word arguments for the problem class"
    )

    algorithm_kwargs: Dict[str, Any] = Field(
        default={},
        description="The key word arguments for the algorithm to use"
    )

    termination: Union[Tuple[str, int], Termination] = Field(
        ...,
        help="The termination criterion of the algorithm"
    )

    is_inverted: bool = Field(
        default=False,
        description="Whether to solve a reverse problem (i.e. minimize negative)"
    )

    save_root: str = Field(
        ...,
        description="Where to save the results"
    )

    def get_problem(self) -> Type[MPOBaseProblem]:
        assert self.problem in self.problems, f"No problem {self.problem} is defined."
        return self.problems[self.problem]

    def get_algorithm(self) -> Type[Algorithm]:
        assert self.algorithm in self.algorithms, f"No algorithm {self.algorithm} is defined."
        return self.algorithms[self.algorithm]

    def get_save_dir(self) -> Path:
        save_root = Path(self.save_root).resolve()
        return save_root / f"{self.algorithm}_{self.problem}_on_{datetime.now().strftime('')}"
