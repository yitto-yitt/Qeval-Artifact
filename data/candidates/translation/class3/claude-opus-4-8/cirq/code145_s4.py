# EVAL_META: task_id=145, framework=cirq, class=3
import cirq
import numpy as np

def qft_inverse(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            angle = -np.pi / (2 ** (k - j))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[k], qubits[j]))
        circuit.append(cirq.H(qubits[j]))
    return circuit
