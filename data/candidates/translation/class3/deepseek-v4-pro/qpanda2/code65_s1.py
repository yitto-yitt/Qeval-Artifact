# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

qvm = CPUQVM()
qvm.init_qvm()
atexit.register(qvm.finalize)

def QFT(n):
    if n == 0:
        return QCircuit()
    q = qvm.qAlloc_many(n)
    circuit = QCircuit()
    
    def qft_rotations(circuit, q, n):
        if n == 0:
            return circuit
        n -= 1
        circuit << H(q[n])
        for qubit in range(n):
            circuit << CP(q[qubit], q[n], np.pi / 2**(n - qubit))
        qft_rotations(circuit, q, n)
    
    def swap_registers(circuit, q, n):
        for qubit in range(n // 2):
            circuit << SWAP(q[qubit], q[n - qubit - 1])
        return circuit
    
    qft_rotations(circuit, q, n)
    swap_registers(circuit, q, n)
    return circuit
