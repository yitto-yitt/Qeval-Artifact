# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def QFT(n):
    circ = pq.QCircuit()
    
    def swap_registers(circ, n):
        for i in range(n // 2):
            circ << pq.SWAP(q[i], q[n - i - 1])
        return circ

    def qft_rotations(circ, n):
        if n == 0:
            return circ
        n -= 1
        circ << pq.H(q[n])
        for i in range(n):
            angle = np.pi / (2 ** (n - i))
            circ << pq.CP(angle, q[i], q[n])
        qft_rotations(circ, n)
        
    qft_rotations(circ, n)
    swap_registers(circ, n)
    return circ

machine.finalize()
