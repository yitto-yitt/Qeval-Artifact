# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    if not hasattr(simons_algorithm, "_qvm"):
        simons_algorithm._qvm = pq.CPUQVM()
        simons_algorithm._qvm.init_qvm()

    qvm = simons_algorithm._qvm
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

    for i in range(n):
        prog << pq.Measure(q_reg1[i], c_reg[i])

    return prog
