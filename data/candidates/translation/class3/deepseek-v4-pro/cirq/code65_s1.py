# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def qft_rotations_rec(circuit, qubits, top):
        if top < 0:
            return
        circuit.append(cirq.H(qubits[top]))
        for j in range(top):
            angle = np.pi / (2 ** (top - j))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubits[j], qubits[top]))
        qft_rotations_rec(circuit, qubits, top - 1)

    qft_rotations_rec(circuit, qubits, n - 1)

    def swap_registers(circuit, qubits, n):
        for i in range(n // 2):
            circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))
        return circuit

    swap_registers(circuit, qubits, n)

    return circuit
