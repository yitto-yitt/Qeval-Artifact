# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, H, CNOT, Measure

def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAllocMany(n + 1)
    c = qvm.cAllocMany(n)
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
    result = qvm.runWithConfiguration(prog, c, 1)
    bitstrings = []
    for key, val in result.items():
        bitstrings.extend([key] * val)
    return [bitstrings, result]
