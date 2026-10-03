# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2 * n)
    c = qvm.cAlloc_many(n)

    reg1 = q[:n]
    reg2 = q[n:]

    prog = pq.QProg()

    for i in range(n):
        prog.insert(pq.H(reg1[i]))
    prog.insert(pq.BARRIER(reg1 + reg2))

    for i in range(n):
        prog.insert(pq.CNOT(reg1[i], reg2[i]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog.insert(pq.CNOT(reg1[i], reg2[j]))
        prog.insert(pq.BARRIER(reg1 + reg2))
        for k in range(n):
            prog.insert(pq.H(reg1[k]))

    for i in range(n):
        prog.insert(pq.Measure(reg1[i], c[i]))

    return prog
