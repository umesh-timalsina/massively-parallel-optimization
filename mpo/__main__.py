import json
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from mpo.optimization_config import OptimizationConfig
from pymoo.optimize import minimize


def orchestrate_optimization(config: OptimizationConfig):
    ProblemClass = config.get_problem()
    optimization_problem = ProblemClass(**config.problem_kwargs)
    Algorithm = config.get_algorithm()
    algorithm = Algorithm(**config.algorithm_kwargs)

    minimize(problem=optimization_problem, algorithm=algorithm, termination=config.termination)




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
