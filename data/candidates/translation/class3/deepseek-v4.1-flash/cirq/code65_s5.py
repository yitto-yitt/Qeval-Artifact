# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    def qft_rotations(circuit, qubits, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit in range(n):
            circuit.append(cirq.CZPowGate(exponent=1/2**(n-qubit)).on(qubits[qubit], qubits[n]))
        qft_rotations(circuit, qubits, n)
    def swap_registers(circuit, qubits, n):
        for qubit in range(n//2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n-qubit-1]))
        return circuit
    qft_rotations(circuit, qubits, n)
    swap_registers(circuit, qubits, n)
    return circuit
