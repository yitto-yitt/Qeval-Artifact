# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    if not hasattr(simons_algorithm, "_qvm"):
        simons_algorithm._qvm = CPUQVM()
        simons_algorithm._qvm.init_qvm()

    qvm = simons_algorithm._qvm
    qubits = qvm.qAlloc_many(2 * n)
    c = qvm.cAlloc_many(n)

    reg1 = [qubits[i] for i in range(n)]
    reg2 = [qubits[n + i] for i in range(n)]

    prog = QProg()

    for i in range(n):
        prog << H(reg1[i])

    for i in range(n):
        prog << CNOT(reg1[i], reg2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(reg1[i], reg2[j])
        for j in range(n):
            prog << H(reg1[j])

    for i in range(n):
        prog << Measure(reg1[i], c[i])

    return prog
