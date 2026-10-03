# EVAL_META: task_id=145, framework=cirq, class=3
import cirq
import math

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    # Forward QFT circuit with swaps (matching Qiskit's QFT)
    for i in range(n):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i + 1, n):
            theta = math.pi / (2 ** (j - i))
            circuit.append(cirq.CPhase(theta)(qubits[j], qubits[i]))
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    # Inverse of forward QFT gives inverse QFT
    return cirq.inverse(circuit)
