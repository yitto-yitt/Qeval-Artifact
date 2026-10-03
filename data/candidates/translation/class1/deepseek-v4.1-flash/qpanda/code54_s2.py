# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, measure, X, Toffoli

def and_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)
    prog = QProg()
    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(q[i])
        if b_bits[2 - i] == '1':
            prog << X(q[3 + i])
    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])
    for i in range(3):
        prog << measure(q[6 + i], c[i])
    result = qvm.run_with_configuration(prog, c, 1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
