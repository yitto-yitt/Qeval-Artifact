# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = CPUQVM()
    qvm.init_qvm()

    q1 = qvm.qAlloc_many(n)
    q2 = qvm.qAlloc_many(n)
    c = qvm.cAlloc_many(n)

    circuit = QProg()

    for j in range(n):
        circuit << H(q1[j])

    for j in range(n):
        circuit << CNOT(q1[j], q2[j])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q1[i], q2[j])

    for j in range(n):
        circuit << H(q1[j])

    for j in range(n):
        circuit << Measure(q1[j], c[j])

    return circuit
