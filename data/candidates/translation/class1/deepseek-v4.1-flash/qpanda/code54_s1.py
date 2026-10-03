# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, X, Toffoli, measure, CPUQVM


def and_gate(a, b):
    q = Qubit(9)
    c = CBit(3)
    prog = QProg()
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(q[i])
        if b_bits[2 - i] == '1':
            prog << X(q[3 + i])
    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])
    for i in range(3):
        prog << measure(q[6 + i], c[i])
    machine = CPUQVM()
    machine.run(prog, 1000)
    result = machine.result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
