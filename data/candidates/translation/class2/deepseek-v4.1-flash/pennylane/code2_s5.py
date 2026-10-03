# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
from math import sqrt

def create_bell_statevector():
    zero_zero = qml.math.array([1, 0, 0, 0])
    one_one = qml.math.array([0, 0, 0, 1])
    return (zero_zero + one_one) / sqrt(2)
