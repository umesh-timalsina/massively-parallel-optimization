from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional, Tuple, Type, Union

from dask.distributed import Client
from pydantic import BaseModel, Field
from pymoo.core.algorithm import Algorithm
from pymoo.core.termination import Termination


class OptimizationConfig(BaseModel):
    problems: ClassVar[Dict[str, Any]] = {}

    algorithms: ClassVar[Dict[str, Any]] = {}

    runners: ClassVar[Dict[str, Any]] = {}

    problem: str = Field(
        ...,
        description="The name of the problem to solve",
    )

    algorithm: str = Field(
        ...,
        description="The name of the algorithm on which this problem needs to be solved",
    )

    runner: str = Field(
        default=None, description="The runner to use for parallel operations"
    )

    problem_kwargs: Dict[str, Any] = Field(
        default={}, description="The key word arguments for the problem class"
    )

    algorithm_kwargs: Dict[str, Any] = Field(
        default={},
        description="The key word arguments for the algorithm to use",
    )

    termination: Union[Tuple[str, int], Termination] = Field(
        ..., help="The termination criterion of the algorithm"
    )

    is_inverted: bool = Field(
        default=False,
        description="Whether to solve a reverse problem (i.e. minimize negative)",
    )

    save_root: str = Field(..., description="Where to save the results")

    verbose: bool = Field(
        default=True, description="The verbosity of the solution"
    )

    def get_problem(self) -> Type["MPOBaseProblem"]:
        assert (
            self.problem in self.problems
        ), f"No problem {self.problem} is defined."
        return self.problems[self.problem]

    def get_algorithm(self) -> Type[Algorithm]:
        assert (
            self.algorithm in self.algorithms
        ), f"No algorithm {self.algorithm} is defined."
        return self.algorithms[self.algorithm]

    def get_runner(self) -> Optional[Client]:
        if self.runner is not None:
            assert (
                self.runner in self.runners
            ), f"No runners {self.runner} is defined."
            return self.runners[self.runner]

    class Config:
        arbitrary_types_allowed = True
