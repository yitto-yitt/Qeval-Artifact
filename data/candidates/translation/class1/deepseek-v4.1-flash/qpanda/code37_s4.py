# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *

def bv_algorithm(s):
    n = len(s)
    ancilla = n

    qvm = CPUQVM()
    qvm.init_qvm()

    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)

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
        prog << Measure(q[i], c[i])

    result = qvm.run_with_configuration(prog, c, 1)

    key = list(result.keys())[0]
    if isinstance(key, str):
        bitstring = key.zfill(n)
    else:
        bitstring = format(int(key), "0{}b".format(n))

    bitstrings = [bitstring]
    return [bitstrings, result]
