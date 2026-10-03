# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, CP, SWAP
from numpy import pi

def QFT(n):
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(n)]
    def swap_registers(circuit, n, qubits):
        for qubit in range(n//2):
            circuit << SWAP(qubits[qubit], qubits[n-qubit-1])
        return circuit
    def qft_rotations(circuit, n, qubits):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CP(qubits[qubit], qubits[n], pi/2**(n-qubit))
        qft_rotations(circuit, n, qubits)
    
    qft_rotations(circuit, n, qubits)
    swap_registers(circuit, n, qubits)
    return circuit
