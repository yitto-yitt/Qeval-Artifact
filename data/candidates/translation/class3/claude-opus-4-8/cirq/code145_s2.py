# EVAL_META: task_id=145, framework=cirq, class=3
import cirq
import numpy as np


def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for j in range(n // 2):
        circuit.append(cirq.SWAP(qubits[j], qubits[n - 1 - j]))
    for i in reversed(range(n)):
        for j in reversed(range(i + 1, n)):
            angle = -np.pi / (2 ** (j - i))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi).on(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))
    return circuit
