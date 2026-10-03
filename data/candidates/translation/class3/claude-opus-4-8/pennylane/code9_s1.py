# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_efficientSU2():
    num_qubits = 3
    reps = 1
    num_params = (reps + 1) * 2 * num_qubits

    def circuit(params):
        idx = 0
        for r in range(reps + 1):
            for q in range(num_qubits):
                qml.RY(params[idx], wires=q)
                idx += 1
            for q in range(num_qubits):
                qml.RZ(params[idx], wires=q)
                idx += 1
            if r < reps:
                for q in range(num_qubits - 1):
                    qml.CNOT(wires=[q, q + 1])
        return qml.state()

    return circuit, num_params
