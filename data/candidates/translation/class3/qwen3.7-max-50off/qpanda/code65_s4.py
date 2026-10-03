# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QProg, QCircuit, H, SWAP, CP
from numpy import pi

def QFT(n):
    qm = QuantumMachine()
    qubits = qm.qAlloc_many(n)
    circ = QCircuit()
    
    def swap_registers(circ, n):
        for qubit in range(n//2):
            circ << SWAP(qubits[qubit], qubits[n-qubit-1])
        return circ

    def qft_rotations(circ, n):
        if n == 0:
            return circ
        n -= 1
        circ << H(qubits[n])
        for qubit in range(n):
            circ << CP(pi/2**(n-qubit), qubits[qubit], qubits[n])
        qft_rotations(circ, n)
        
    qft_rotations(circ, n)
    swap_registers(circ, n)
    
    prog = QProg()
    prog << circ
    return prog
