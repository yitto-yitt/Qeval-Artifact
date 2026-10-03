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

    q_reg1 = qvm.qAlloc_many(n)
    q_reg2 = qvm.qAlloc_many(n)
    c_reg = qvm.cAlloc_many(n)

    prog = pq.QProg()

    for i in range(n):
        prog << pq.H(q_reg1[i])

    for i in range(n):
        prog << pq.CNOT(q_reg1[i], q_reg2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << pq.CNOT(q_reg1[i], q_reg2[j])
        for j in range(n):
            prog << pq.H(q_reg1[j])

    measure_gate = pq.Measure if hasattr(pq, "Measure") else pq.measure
    for i in range(n):
        prog << measure_gate(q_reg1[i], c_reg[i])

    if not hasattr(simons_algorithm, "_qvms"):
        simons_algorithm._qvms = []
    simons_algorithm._qvms.append(qvm)

    return prog
