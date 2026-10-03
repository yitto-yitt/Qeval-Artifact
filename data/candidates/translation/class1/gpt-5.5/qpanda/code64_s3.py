# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()

    reg1 = qvm.qAlloc_many(n)
    reg2 = qvm.qAlloc_many(n)

    try:
        c = qvm.cAlloc_many(n, "c")
    except TypeError:
        c = qvm.cAlloc_many(n)

    prog = QProg()

    h_gate = globals().get("H")
    cx_gate = globals().get("CNOT", globals().get("CX"))
    measure_op = globals().get("Measure", globals().get("measure"))

    for qubit in reg1:
        prog << h_gate(qubit)

    for j in range(n):
        prog << cx_gate(reg1[j], reg2[j])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << cx_gate(reg1[i], reg2[j])
        for qubit in reg1:
            prog << h_gate(qubit)

    for j in range(n):
        prog << measure_op(reg1[j], c[j])

    if not hasattr(simons_algorithm, "_machines"):
        simons_algorithm._machines = []
    simons_algorithm._machines.append(qvm)

    return prog
