# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_state_prep(num_qubits):
    dim = 2 ** num_qubits
    state = np.zeros(dim, dtype=complex)
    state[1] = 1.0

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(state, wires=range(num_qubits))
        return qml.state()

    return circuit
