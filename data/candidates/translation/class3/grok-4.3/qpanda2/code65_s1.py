# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(30)

def QFT(n):
    circuit = QCircuit()
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
            angle = math.pi / 2**(n-qubit)
            circuit << RZ(qubits[n], angle).control(qubits[qubit])
        qft_rotations(circuit, n)
        return circuit
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

machine.finalize()
