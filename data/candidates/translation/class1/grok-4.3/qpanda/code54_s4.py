# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *
def and_gate(a, b):
    machine = init_quantum_machine(QMachineType.CPU)
    qa = machine.qAlloc_many(3)
    qb = machine.qAlloc_many(3)
    qanc = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    astr = format(a, '03b')
    bstr = format(b, '03b')
    for i in range(3):
        if astr[2-i] == '1':
            prog << X(qa[i])
        if bstr[2-i] == '1':
            prog << X(qb[i])
    for i in range(3):
        prog << Toffoli(qa[i], qb[i], qanc[i])
    prog << measure_all(qanc, cbits)
    res = machine.run_with_configuration(prog, 1024)
    machine.finalize()
    tot = sum(res.values())
    return {k: v / tot for k, v in res.items()}
