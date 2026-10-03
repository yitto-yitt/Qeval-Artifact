# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_state_prep(num_qubits):
    basis_state = np.zeros(num_qubits, dtype=int)
    basis_state[-1] = 1
    return qml.tape.QuantumScript(
        [qml.BasisState(basis_state, wires=list(range(num_qubits)))]
    )
