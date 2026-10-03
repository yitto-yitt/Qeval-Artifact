# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import init_quantum_machine, QMachineType, QProg, qAlloc_many, cAlloc_many, X, Toffoli, measure_all, run_with_configuration

def or_gate(a, b):
    if not hasattr(or_gate, '_init'):
        init_quantum_machine(QMachineType.CPU)
        or_gate._init = True

    q_a = qAlloc_many(3)
    q_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    measure = cAlloc_many(3)

    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')

    for i in range(3):
        if a_str[2 - i] == '0':
            prog << X(q_a[i])
        if b_str[2 - i] == '0':
            prog << X(q_b[i])

    for i in range(3):
        prog << Toffoli(q_a[i], q_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    prog << measure_all(ancillary, measure)

    counts = run_with_configuration(prog, measure, 1024)
    total = sum(counts.values())
    return {key[::-1]: value / total for key, value in counts.items()}
