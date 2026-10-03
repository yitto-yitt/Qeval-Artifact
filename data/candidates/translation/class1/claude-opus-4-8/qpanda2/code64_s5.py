# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    machine = pq.CPUQVM()
    machine.init_qvm()
    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)
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
        for i in range(n):
            prog << pq.H(q_reg1[i])

    for i in range(n):
        prog << pq.Measure(q_reg1[i], c_reg[i])

    return prog
