# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import *

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(5)

    prog_full = QProg()
    prog_full << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])

    prog_limited = QProg()
    prog_limited << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])

    qvm.finalize()
    return prog_full, prog_limited
