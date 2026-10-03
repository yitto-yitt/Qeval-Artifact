# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    def circuit():
        for j in reversed(range(num_qubits)):
            for k in reversed(range(j + 1, num_qubits)):
                qml.ControlledPhaseShift(-np.pi / (2 ** (k - j)), wires=[k, j])
            qml.Hadamard(wires=j)
    return circuit
