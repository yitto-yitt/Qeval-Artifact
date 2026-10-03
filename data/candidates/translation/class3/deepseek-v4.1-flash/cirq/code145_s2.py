# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for j in range(n // 2):
        circuit.append(cirq.SWAP(qubits[j], qubits[n - 1 - j]))
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            circuit.append((cirq.CZ ** (-1.0 / (2 ** (k - j)))).on(qubits[k], qubits[j]))
        circuit.append(cirq.H(qubits[j]))
    return circuit
