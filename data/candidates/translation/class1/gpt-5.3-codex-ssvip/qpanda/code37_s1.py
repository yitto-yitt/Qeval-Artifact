# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *
import random


def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)

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

    prog << measure_all(q[:n], c)

    result_dict = qvm.run_with_configuration(prog, c, 1)

    bitstrings = []
    for k, v in result_dict.items():
        bitstrings.extend([k] * int(v))

    qvm.finalize()
    return [bitstrings, result_dict]
