# EVAL_META: task_id=64, framework=qpanda2, class=1
import pyqpanda as pq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2 * n)
    cbits = machine.cAlloc_many(n)
    reg1 = qubits[0:n]
    reg2 = qubits[n:2 * n]

    prog = pq.QProg()

    for q in reg1:
        prog << pq.H(q)

    for j in range(n):
        prog << pq.CNOT(reg1[j], reg2[j])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << pq.CNOT(reg1[i], reg2[j])
        for q in reg1:
            prog << pq.H(q)

    for j in range(n):
        prog << pq.Measure(reg1[j], cbits[j])

    return prog
