# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    ops = []
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            ops.append(qml.ControlledPhaseShift(-np.pi / (2 ** (j - i)), wires=[j, i]))
        ops.append(qml.Hadamard(wires=i))
    return ops
