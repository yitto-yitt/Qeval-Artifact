# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))

    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            circuit.append(cirq.CZPowGate(exponent=-(1 / (2 ** (j - i))))(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))

    return circuit
