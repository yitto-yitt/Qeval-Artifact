# EVAL_META: task_id=64, framework=qpanda, class=1
import pyqpanda3.core as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    q_alloc = getattr(qvm, "qAlloc_many", None) or getattr(qvm, "qalloc_many")
    c_alloc = getattr(qvm, "cAlloc_many", None) or getattr(qvm, "calloc_many")

    q_reg1 = q_alloc(n)
    q_reg2 = q_alloc(n)

    try:
        c_reg = c_alloc(n, "c")
    except TypeError:
        c_reg = c_alloc(n)

    prog = pq.QProg()

    def append(op):
        nonlocal prog
        try:
            ret = prog << op
            if ret is not None:
                prog = ret
        except Exception:
            ret = prog.insert(op)
            if ret is not None:
                prog = ret

    cx = getattr(pq, "CNOT", None) or getattr(pq, "CX")
    meas = getattr(pq, "measure", None) or getattr(pq, "Measure")

    for qubit in q_reg1:
        append(pq.H(qubit))

    for j in range(n):
        append(cx(q_reg1[j], q_reg2[j]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                append(cx(q_reg1[i], q_reg2[j]))
        for qubit in q_reg1:
            append(pq.H(qubit))

    for j in range(n):
        append(meas(q_reg1[j], c_reg[j]))

    try:
        prog._qvm = qvm
        prog._qubits = (q_reg1, q_reg2)
        prog._cbits = c_reg
    except Exception:
        if not hasattr(simons_algorithm, "_qvms"):
            simons_algorithm._qvms = []
        simons_algorithm._qvms.append(qvm)

    return prog
