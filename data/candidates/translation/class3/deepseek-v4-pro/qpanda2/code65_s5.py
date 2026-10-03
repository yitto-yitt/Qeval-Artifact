# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()

def QFT(n):
    q = machine.qAlloc_many(n)
    circuit = QCircuit()
    
    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit << SWAP(q[qubit], q[n - qubit - 1])
        return circuit
    
    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(q[n])
        for qubit in range(n):
            circuit << CP(q[qubit], q[n], pi / 2 ** (n - qubit))
        qft_rotations(circuit, n)
        return circuit
    
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

machine.finalize()
