from typing import Any, ClassVar, Dict, List

from pydantic import BaseModel, Field


class OptimizationConfig(BaseModel):
    problems: ClassVar[Dict[str, Any]] = {}

    problem: str = Field(
        ...,
        description="The name of the problem to solve",
    )

    problem_kwargs: Dict[str, Any] = Field(
        default={}, description="The key word arguments for the problem class"
    )

    def get_problem(self):
        assert self.problem in self.problems, f"No problem {self.problem} is defined."
        return self.problems[self.problem]
