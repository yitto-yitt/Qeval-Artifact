# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def QFT(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    circuit = QCircuit()
    def swap_registers(circ, n):
        for i in range(n//2):
            circ << SWAP(qubits[i], qubits[n-i-1])
        return circ
    def qft_rotations(circ, n):
        if n == 0:
            return circ
        n -= 1
        circ << H(qubits[n])
        for qubit in range(n):
            circ << CR(qubits[qubit], qubits[n], pi/2**(n-qubit))
        qft_rotations(circ, n)
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    qvm.finalize()
    return circuit
