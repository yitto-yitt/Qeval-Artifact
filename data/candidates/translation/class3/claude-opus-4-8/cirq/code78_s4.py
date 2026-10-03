# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    ops = []
    for j in range(num_qubits):
        ops.append(cirq.H(qubits[j]))
        for k in range(j + 1, num_qubits):
            angle = np.pi / (2 ** (k - j))
            ops.append(cirq.CZPowGate(exponent=angle / np.pi).on(qubits[k], qubits[j]))
    forward = cirq.Circuit(ops)
    return cirq.inverse(forward)
