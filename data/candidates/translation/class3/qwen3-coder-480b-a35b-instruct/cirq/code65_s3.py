# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def swap_registers(circuit, n):
        for qubit_idx in range(n//2):
            circuit.append(cirq.SWAP(qubits[qubit_idx], qubits[n-qubit_idx-1]))
        return circuit
    
    def qft_rotations(circuit, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return circuit
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit_idx in range(n):
            angle = np.pi / 2**(n-qubit_idx)
            circuit.append(cirq.CZPowGate(exponent=angle/np.pi)(qubits[qubit_idx], qubits[n]))
        qft_rotations(circuit, n)
    
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
