import json
import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from pymoo.optimize import minimize

from mpo.optimization_config import OptimizationConfig
from mpo.result import Result as MPOResult


def orchestrate_optimization(config: OptimizationConfig):
    runner_func = config.get_runner()
    ProblemClass = config.get_problem()
    kwargs = deepcopy(config.problem_kwargs)
    kwargs["runner"] = runner_func() if runner_func else None
    optimization_problem = ProblemClass(**kwargs)
    Algorithm = config.get_algorithm()
    algorithm = Algorithm(**config.algorithm_kwargs)
    root = Path(config.save_root)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    expr_signature = (
        f"{ProblemClass.__name__}_SolvedBy_{Algorithm.__name__}_on_{timestamp}"
    )
    save_dir = root / expr_signature
    os.makedirs(save_dir, exist_ok=True)

    with (save_dir / "Config.json").open("w") as config_file:
        json.dump(config.dict(), config_file, indent=2)

    result = minimize(
        problem=optimization_problem,
        algorithm=algorithm,
        termination=config.termination,
        verbose=config.verbose,
    )
    if kwargs["runner"]:
        kwargs["runner"].close()
    mpo_result = MPOResult(algorithm_result=result)
    mpo_result.save(save_dir)
    del mpo_result.algorithm_result.problem

    print(f"Execution Time: {result.exec_time}")


def run(args=None):
    parser = ArgumentParser(
        "Massively Parallel Optimization with PyMoo and Dask",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", help="The config file (json)")

    args = parser.parse_args(args)

    with open(args.config, "r") as config_json:
        config_dict = json.load(config_json)
        optimization_config = OptimizationConfig.parse_obj(config_dict)
        orchestrate_optimization(optimization_config)
