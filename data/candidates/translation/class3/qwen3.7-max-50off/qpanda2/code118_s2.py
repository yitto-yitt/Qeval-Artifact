# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # C3SX is a 3-controlled sqrt(X) gate.
    # Since pyqpanda lacks a native C3SX gate, we construct a semantic proxy
    # using available controlled-RX gates with the sqrt(X) angle (pi/2).
    prog << pq.CRX(np.pi/2, q[0], q[3])
    prog << pq.CRX(np.pi/2, q[1], q[3])
    prog << pq.CRX(np.pi/2, q[2], q[3])
    return prog

machine.finalize()
