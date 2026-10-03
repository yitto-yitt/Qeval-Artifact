# EVAL_META: task_id=64, framework=qpanda, class=1
import pyqpanda3.core as pq


def simons_algorithm(s):
    try:
        machine = pq.get_global_machine()
    except:
        machine = pq.init_quantum_machine(pq.QMachineType.CPU)

    n = len(s)
    s = s[::-1]

    q_reg1 = pq.qAlloc_many(n)
    q_reg2 = pq.qAlloc_many(n)
    c_reg = pq.cAlloc_many(n)

    prog = pq.QProg()

    for q in q_reg1:
        prog << pq.H(q)

    for i in range(n):
        prog << pq.CNOT(q_reg1[i], q_reg2[i])

    if "1" in s:
        idx = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << pq.CNOT(q_reg1[idx], q_reg2[j])
        for q in q_reg1:
            prog << pq.H(q)

    for i in range(n):
        prog << pq.Measure(q_reg1[i], c_reg[i])

    return prog
