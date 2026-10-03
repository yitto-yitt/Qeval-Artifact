# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def noisy_bell():
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    counts = qvm.run_with_configuration(prog, c, 1000)
    qvm.finalize()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
