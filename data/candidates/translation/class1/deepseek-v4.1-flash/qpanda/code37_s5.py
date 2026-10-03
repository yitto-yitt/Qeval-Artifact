# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure

def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)
    ancilla = n

    prog = QProg()
    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << measure(q[i], c[i])

    result = qvm.run_with_configuration(prog, c, 1)
    raw_bitstring = list(result.keys())[0]
    bitstring = raw_bitstring[::-1]
    bitstrings = [bitstring]
    return [bitstrings, result]
