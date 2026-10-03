# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    ops = []
    for j in range(num_qubits):
        for k in range(j):
            ops.append(cirq.CZPowGate(exponent=-1.0 / (2 ** (j - k)))(qubits[k], qubits[j]))
        ops.append(cirq.H(qubits[j]))
    return cirq.Circuit(cirq.inverse(ops))
