# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            exponent = -1 / (2 ** (k - j))
            circuit.append(cirq.CZPowGate(exponent=exponent).on(qubits[k], qubits[j]))
        circuit.append(cirq.H(qubits[j]))
    return circuit
