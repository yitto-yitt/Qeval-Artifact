# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    ops = []
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            lam = -np.pi / (2 ** (k - j))
            ops.append(cirq.CZPowGate(exponent=lam / np.pi).on(qubits[k], qubits[j]))
        ops.append(cirq.H(qubits[j]))
    return cirq.Circuit(ops)
