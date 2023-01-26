from .optimization_config import OptimizationConfig


class RegistersMPOConstruct:
    def __init__(self, construct_name, construct_key=None):
        self.construct_name = construct_name
        self.construct_key = construct_key

    def __call__(self, method_or_class):
        construct_registry = getattr(OptimizationConfig, self.construct_name)
        construct_registry[
            self.construct_key or getattr(method_or_class, "__name__")
        ] = method_or_class
