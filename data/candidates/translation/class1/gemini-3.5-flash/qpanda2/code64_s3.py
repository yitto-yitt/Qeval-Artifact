# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    n = len(s)
    s = s[::-1]
    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)

    prog = pq.QProg()
    for q in q_reg1:
        prog << pq.H(q)

    for q1, q2 in zip(q_reg1, q_reg2):
        prog << pq.CNOT(q1, q2)

    if "1" in s:
        i = s.find("1")
        ctrl_q = q_reg1[i]
        for j in range(n):
            if s[j] == "1":
                prog << pq.CNOT(ctrl_q, q_reg2[j])

        for q in q_reg1:
            prog << pq.H(q)

    for q, c in zip(q_reg1, c_reg):
        prog << pq.Measure(q, c)

    return prog
