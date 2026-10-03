# EVAL_META: task_id=145, framework=cirq, class=3
import cirq
import numpy as np

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for j in range(n // 2):
        circuit.append(cirq.SWAP(qubits[j], qubits[n - 1 - j]))
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            control = qubits[n - 1 - k]
            target = qubits[n - 1 - j]
            circuit.append(cirq.CZ**(angle / np.pi).on(control, target))
        circuit.append(cirq.H(qubits[n - 1 - j]))
    return circuit
