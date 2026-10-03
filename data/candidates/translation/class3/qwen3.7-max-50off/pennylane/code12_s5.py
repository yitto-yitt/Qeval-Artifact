# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def get_unitary():
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
    return np.array(qml.matrix(circuit, wire_order=[0, 1])())
