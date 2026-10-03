# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for i in range(n - 1, -1, -1):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i):
            exponent = 1 / (2 ** (i - j))
            circuit.append(cirq.CZPowGate(exponent=exponent).on(qubits[j], qubits[i]))
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))
    return circuit
