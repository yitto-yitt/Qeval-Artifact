# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def get_unitary():
    ops = [qml.Hadamard(wires=0), qml.CNOT(wires=[0, 1])]
    return qml.matrix(qml.ops.Prod(*reversed(ops)), wire_order=[0, 1])
