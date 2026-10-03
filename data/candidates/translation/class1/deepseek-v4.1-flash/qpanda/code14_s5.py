# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def bell_each_shot():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    result = qvm.run(prog, 10)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
