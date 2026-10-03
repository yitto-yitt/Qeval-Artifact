# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    ops = []
    for i in range(n // 2):
        ops.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    for j in range(n):
        for m in range(j):
            ops.append(cirq.CZPowGate(exponent=-1.0 / (2 ** (j - m)))(qubits[m], qubits[j]))
        ops.append(cirq.H(qubits[j]))
    return cirq.Circuit(ops)
