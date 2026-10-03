# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, measure, X, CCX

def or_gate(a, b):
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(i)
        if b_bin[2 - i] == '0':
            prog << X(3 + i)
    for i in range(3):
        prog << CCX(i, 3 + i, 6 + i)
    for i in range(3):
        prog << X(6 + i)
    for i in range(3):
        prog << measure(6 + i, i)
    qvm = CPUQVM()
    qvm.run(prog, 1024)
    result = qvm.result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
