# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def noisy_bell():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])
    shots = 1000
    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()
    total = builtins.sum(counts.values())
    result = {}
    for k, v in counts.items():
        if isinstance(k, int):
            key = format(k, '02b')
        else:
            key = str(k).zfill(2)
        result[key] = v / total
    return result
