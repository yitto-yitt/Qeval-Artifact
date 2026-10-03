# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def qft_no_swaps(num_qubits):
    ops = []
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            phase = -2 * np.pi / 2 ** (j - i)
            ops.append(qml.CPhase(phase, wires=[i, j]))
        ops.append(qml.Hadamard(i))
    return qml.tape.QuantumScript(ops, [])
