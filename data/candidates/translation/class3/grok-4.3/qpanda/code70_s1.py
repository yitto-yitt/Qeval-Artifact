# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CSWAP, Sdag

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CSWAP(q[0], q[1], q[2]) << H(q[1]) << Sdag(q[0]).control(q[1])
    return prog
