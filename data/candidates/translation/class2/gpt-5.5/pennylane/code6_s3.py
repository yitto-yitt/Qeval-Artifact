# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_state_prep(num_qubits):
    basis_state = np.zeros(num_qubits, dtype=int)
    basis_state[0] = 1
    return qml.tape.QuantumScript(
        [qml.BasisState(basis_state, wires=range(num_qubits))]
    )
