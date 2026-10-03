# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
from numpy import pi

def QFT(n):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(n)
    circuit = QProg()
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit << SWAP(qubits[qubit], qubits[n-qubit-1])
        return circuit
    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(qubits[n])
        for qubit in range(n):
            circuit << CR(qubits[qubit], qubits[n], pi/2**(n-qubit))
        qft_rotations(circuit, n)
        return circuit
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
