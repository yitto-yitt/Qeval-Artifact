# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    q_alloc = getattr(machine, "qAlloc_many", None)
    if q_alloc is None:
        q_alloc = getattr(machine, "qalloc_many")

    c_alloc = getattr(machine, "cAlloc_many", None)
    if c_alloc is None:
        c_alloc = getattr(machine, "calloc_many")

    q_reg1_vec = q_alloc(n)
    q_reg2_vec = q_alloc(n)
    c_reg_vec = c_alloc(n)

    q_reg1 = [q_reg1_vec[i] for i in range(n)]
    q_reg2 = [q_reg2_vec[i] for i in range(n)]
    c_reg = [c_reg_vec[i] for i in range(n)]

    prog = QProg()

    def append(op):
        nonlocal prog
        if hasattr(prog, "insert"):
            ret = prog.insert(op)
            if ret is not None:
                prog = ret
        else:
            prog << op

    cnot_gate = globals().get("CNOT", None) or globals().get("CX", None)
    measure_gate = globals().get("Measure", None) or globals().get("measure", None)

    for qubit in q_reg1:
        append(H(qubit))

    for j in range(n):
        append(cnot_gate(q_reg1[j], q_reg2[j]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                append(cnot_gate(q_reg1[i], q_reg2[j]))
        for qubit in q_reg1:
            append(H(qubit))

    for j in range(n):
        append(measure_gate(q_reg1[j], c_reg[j]))

    try:
        simons_algorithm._machines.append(machine)
    except AttributeError:
        simons_algorithm._machines = [machine]

    return prog
