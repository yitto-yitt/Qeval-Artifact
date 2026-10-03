# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(50)

def QFT(n):
    circ = pq.QCircuit()
    
    def qft_rotations(n_val):
        if n_val == 0:
            return
        n_val -= 1
        circ << pq.H(q[n_val])
        for qubit in range(n_val):
            theta = np.pi / (2 ** (n_val - qubit))
            circ << pq.CR(q[qubit], q[n_val], theta)
        qft_rotations(n_val)
        
    qft_rotations(n)
    
    for i in range(n // 2):
        circ << pq.SWAP(q[i], q[n - i - 1])
        
    return circ

machine.finalize()
