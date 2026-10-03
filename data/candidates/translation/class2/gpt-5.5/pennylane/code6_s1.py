# EVAL_META: task_id=6, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def create_state_prep(num_qubits):
    state = np.zeros(2 ** num_qubits, dtype=complex)
    state[1] = 1.0
    return qml.tape.QuantumScript([qml.StatePrep(state, wires=range(num_qubits))])
