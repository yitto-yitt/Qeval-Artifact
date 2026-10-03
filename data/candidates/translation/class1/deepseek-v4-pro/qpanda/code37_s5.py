# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *


def bv_algorithm(s):
    n = len(s)
    init(QMachineType.CPU)

    q = qAlloc_many(n + 1)
    c = cAlloc_many(n + 1)
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

    prog << measure_all(q, c)

    result = run_with_configuration(prog, c, 1)
    bitstrings = [key[:n][::-1] for key in result.keys()]

    destroy()
    return [bitstrings, result]
