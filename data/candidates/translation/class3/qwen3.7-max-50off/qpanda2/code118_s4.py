# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    
    rx_gate = pq.RX(q[3], np.pi / 2)
    c3_rx = rx_gate.control([q[0], q[1], q[2]])
    prog << c3_rx
    
    u1_gate = pq.U1(q[0], np.pi / 4)
    c2_u1 = u1_gate.control([q[1], q[2]])
    prog << c2_u1
    
    return prog

machine.finalize()
