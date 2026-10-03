# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *

def bv_algorithm(s):
    n = len(s)
    init(QMachineType.CPU)
    q = qAlloc_many(n + 1)
    c = cAlloc_many(n)
    prog = QProg()
    ancilla = n

    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])

    for index, bit in enumerate(s):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])

    for i in range(n):
        prog << H(q[i])

    for i in range(n):
        prog << Measure(q[i], c[i])

    shots = 1
    counts = run_with_configuration(prog, c, shots)
    bitstrings = list(counts.keys())
    return [bitstrings, counts]
