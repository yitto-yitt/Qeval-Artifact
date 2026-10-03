# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit in range(n):
            circuit.append(cirq.CZPowGate(exponent=(pi / (2 ** (n - qubit))) / pi).on(qubits[qubit], qubits[n]))
        qft_rotations(circuit, n)
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
