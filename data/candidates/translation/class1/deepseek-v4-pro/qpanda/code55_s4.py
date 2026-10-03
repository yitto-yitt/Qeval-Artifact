# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, Toffoli, Measure

def or_gate(a, b):
    machine = QuantumMachine()
    qa = machine.qAlloc_many(3)
    qb = machine.qAlloc_many(3)
    anc = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(qa[i])
        if b_bin[2 - i] == '0':
            prog << X(qb[i])

    for i in range(3):
        prog << Toffoli(qa[i], qb[i], anc[i])

    for i in range(3):
        prog << X(anc[i])

    prog << Measure(anc[0], cbits[2])
    prog << Measure(anc[1], cbits[1])
    prog << Measure(anc[2], cbits[0])

    counts = machine.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
