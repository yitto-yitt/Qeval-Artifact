# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    return [circuit] * n
