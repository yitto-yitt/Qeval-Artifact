# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def noisy_bell():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << measure_all(q, c)
    shots = 1000
    result = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
