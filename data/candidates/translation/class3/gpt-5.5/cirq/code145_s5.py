# EVAL_META: task_id=145, framework=cirq, class=3
import cirq


def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))

    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            circuit.append(
                cirq.CZPowGate(exponent=-(1 / (2 ** (k - j)))).on(qubits[k], qubits[j])
            )
        circuit.append(cirq.H(qubits[j]))

    return circuit
