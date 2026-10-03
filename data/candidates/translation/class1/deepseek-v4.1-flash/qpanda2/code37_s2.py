# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *

def bv_algorithm(s):
    n = len(s)
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    ancilla = n

    prog = QProg()
    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])
    for i in range(n):
        if s[i] == '1':
            prog << CNOT(q[i], q[ancilla])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << measure(q[i], c[i])

    result = machine.run_with_configuration(prog, c, 1)
    bitstrings = list(result.keys())
    machine.finalize()
    return [bitstrings, result]
