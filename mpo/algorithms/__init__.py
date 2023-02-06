from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.soo.nonconvex.ga import GA

from mpo.utils import RegistersMPOConstruct

RegistersMPOConstruct(construct_name="algorithms", construct_key="GA")(GA)
RegistersMPOConstruct(construct_name="algorithms", construct_key="NSGA2")(NSGA2)
