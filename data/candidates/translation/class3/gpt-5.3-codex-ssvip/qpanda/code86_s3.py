# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import *

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(5)

    prog = QProg()
    prog << H(q[0]) \
         << CNOT(q[0], q[1]) \
         << CNOT(q[1], q[2]) \
         << CNOT(q[2], q[3]) \
         << CNOT(q[3], q[4])

    full_block = QProg()
    full_block << H(q[0]) \
               << CNOT(q[0], q[1]) \
               << CNOT(q[1], q[2]) \
               << CNOT(q[2], q[3]) \
               << CNOT(q[3], q[4])

    limited_block = QProg()
    limited_block << H(q[0]) \
                  << CNOT(q[0], q[1]) \
                  << CNOT(q[1], q[2]) \
                  << CNOT(q[2], q[3]) \
                  << CNOT(q[3], q[4])

    return full_block, limited_block
