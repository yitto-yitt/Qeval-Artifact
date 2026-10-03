# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def create_efficientSU2():
    num_qubits = 3
    reps = 1
    insert_barriers = True
    num_params = 2 * num_qubits * (reps + 1)

    dev = qml.device("default.qubit", wires=num_qubits)

    # reversed_linear entanglement (EfficientSU2 default)
    ent_pairs = [(i, i + 1) for i in range(num_qubits - 1)][::-1]

    @qml.qnode(dev)
    def circuit(params=None):
        if params is None:
            params = np.zeros(num_params)
        idx = 0
        for _ in range(reps):
            for q in range(num_qubits):
                qml.RY(params[idx], wires=q); idx += 1
            for q in range(num_qubits):
                qml.RZ(params[idx], wires=q); idx += 1
            if insert_barriers:
                qml.Barrier(wires=range(num_qubits))
            for (c, t) in ent_pairs:
                qml.CNOT(wires=[c, t])
            if insert_barriers:
                qml.Barrier(wires=range(num_qubits))
        for q in range(num_qubits):
            qml.RY(params[idx], wires=q); idx += 1
        for q in range(num_qubits):
            qml.RZ(params[idx], wires=q); idx += 1
        return qml.state()

    return circuit
