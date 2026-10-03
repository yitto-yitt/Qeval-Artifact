# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QVM, QProg, X, Measure

def not_gate(a):
    vm = QVM()
    q = vm.qAlloc_many(8)
    c = vm.cAlloc_many(8)

    prog = QProg()
    a = format(a, '08b')
    for i in range(8):
        if a[7 - i] == '0':
            prog << X(q[i])

    for i in range(8):
        prog << Measure(q[i], c[i])

    counts = vm.run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
