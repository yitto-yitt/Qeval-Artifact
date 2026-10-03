# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import init, qAlloc_many, cAlloc_many, QProg, X, CCX, measure_all, run_with_configuration

def or_gate(a, b):
    if not getattr(or_gate, '_initialized', False):
        init()
        or_gate._initialized = True

    q_a = qAlloc_many(3)
    q_b = qAlloc_many(3)
    anc = qAlloc_many(3)
    meas = cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(q_a[i])
        if b_bits[2 - i] == '0':
            prog << X(q_b[i])

    for i in range(3):
        prog << CCX(q_a[i], q_b[i], anc[i])

    for q in anc:
        prog << X(q)

    prog << measure_all(anc, meas)

    counts = run_with_configuration(prog, meas, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
