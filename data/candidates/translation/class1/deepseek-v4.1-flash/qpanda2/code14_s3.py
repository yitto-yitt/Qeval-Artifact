# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def bell_each_shot():
    shots = 10
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << measure(q[0], c[0]) << measure(q[1], c[1])
    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
