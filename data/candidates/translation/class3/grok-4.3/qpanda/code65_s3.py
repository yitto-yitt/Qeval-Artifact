# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, CR
from numpy import pi

def QFT(n):
    circuit = QCircuit()
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit << SWAP(qubit, n-qubit-1)
        return circuit
    def qft_rotations(circuit, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return circuit
        n -= 1
        circuit << H(n)
        for qubit in range(n):
            circuit << CR(pi/2**(n-qubit), qubit, n)
        qft_rotations(circuit, n)
        return circuit
    
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
