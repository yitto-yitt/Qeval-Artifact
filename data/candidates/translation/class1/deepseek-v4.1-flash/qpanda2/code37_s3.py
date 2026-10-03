# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, X, CNOT, measure
import builtins


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
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << measure(q[i], c[i])

    result = machine.run_with_configuration(prog, c, 1)
    machine.finalize()

    bitstrings = list(result.keys())
    return [bitstrings, result]
