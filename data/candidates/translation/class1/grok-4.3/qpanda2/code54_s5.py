# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qa = machine.qAlloc_many(3)
    qb = machine.qAlloc_many(3)
    qanc = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = QProg()
    astr = format(a, '03b')
    bstr = format(b, '03b')
    for i in range(3):
        if astr[2 - i] == '1':
            prog << X(qa[i])
        if bstr[2 - i] == '1':
            prog << X(qb[i])
    for i in range(3):
        prog << Toffoli(qa[i], qb[i], qanc[i])
    for i in range(3):
        prog << Measure(qanc[i], c[i])
    shots = 1024
    result = machine.run_with_configuration(prog, shots=shots, cbit_list=c)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
