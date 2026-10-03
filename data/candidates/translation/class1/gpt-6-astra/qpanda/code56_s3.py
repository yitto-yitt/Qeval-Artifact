# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure

def not_gate(a):
    prog = QProg()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            prog << X(i)
    for i in range(8):
        prog << measure(i, i)

    qvm = CPUQVM()
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key.zfill(8): value / total for key, value in counts.items()}
