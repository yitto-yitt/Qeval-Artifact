# EVAL_META: task_id=6, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def create_state_prep(num_qubits):
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        state_vector = np.zeros(2**num_qubits, dtype=complex)
        state_vector[1] = 1 + 0j
        qml.StatePrep(state_vector, wires=range(num_qubits))
        return qml.state()

    return circuit
