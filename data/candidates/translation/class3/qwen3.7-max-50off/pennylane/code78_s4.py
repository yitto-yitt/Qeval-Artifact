# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    ops = []
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            ops.append(qml.ControlledPhaseShift(-np.pi / (2 ** (k - j)), wires=[k, j]))
        ops.append(qml.Hadamard(wires=j))
    return ops
