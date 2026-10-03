# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)

def QFT(n):
    circ = pq.QCircuit()
    
    def qft_rotations(n_val):
        if n_val == 0:
            return
        n_val -= 1
        circ << pq.H(q[n_val])
        for qubit in range(n_val):
            circ << pq.CR(q[qubit], q[n_val], np.pi / (2**(n_val - qubit)))
        qft_rotations(n_val)
        
    def swap_registers(n_val):
        for i in range(n_val // 2):
            circ << pq.SWAP(q[i], q[n_val - i - 1])
            
    qft_rotations(n)
    swap_registers(n)
    return circ

machine.finalize()
