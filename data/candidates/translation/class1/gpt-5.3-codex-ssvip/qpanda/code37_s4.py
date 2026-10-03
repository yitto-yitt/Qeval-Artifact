# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *

def bv_algorithm(s):
    n = len(s)
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)

    prog = QProg()
    ancilla = n

    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])

    for i in range(n):
        prog << H(q[i])

    for i in range(n):
        prog << Measure(q[i], c[i])

    result = machine.run_with_configuration(prog, c, 1)
    bitstrings = []
    for k, v in result.items():
        bitstrings.extend([k] * v)

    machine.finalize()
    return [bitstrings, result]
