# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n-qubit-1]))
        return circuit
    def qft_rotations(circuit, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return circuit
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit in range(n):
            circuit.append((cirq.CZ ** (1 / 2 ** (n - qubit))).on(qubits[qubit], qubits[n]))
        qft_rotations(circuit, n)
    
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
