# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    ops = []
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j+1, num_qubits)):
            ops.append(qml.ControlledPhaseShift(-np.pi / 2**(k - j), wires=[j, k]))
        ops.append(qml.Hadamard(wires=j))
    return ops
