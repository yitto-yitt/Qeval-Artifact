# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    ops = []
    for j in range(num_qubits):
        wire_j = num_qubits - 1 - j
        for k in range(j):
            wire_k = num_qubits - 1 - k
            ops.append(qml.ControlledPhaseShift(-np.pi / (2 ** (j - k)), wires=[wire_j, wire_k]))
        ops.append(qml.Hadamard(wires=wire_j))
    return qml.tape.QuantumScript(ops, [])
