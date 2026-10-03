# EVAL_META: task_id=6, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def create_state_prep(num_qubits):
    basis_state = np.zeros(num_qubits, dtype=int)
    basis_state[-1] = 1
    return qml.tape.QuantumScript(
        [qml.BasisState(basis_state, wires=range(num_qubits))]
    )
