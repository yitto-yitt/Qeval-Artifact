# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Barrier, Measure

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2 * n)
    cbits = qvm.cAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])
    prog << Barrier(qubits)
    for i in range(n):
        prog << CNOT(qubits[i], qubits[n + i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(qubits[i], qubits[n + j])
        prog << Barrier(qubits)
        for i in range(n):
            prog << H(qubits[i])
    for i in range(n):
        prog << Measure(qubits[i], cbits[i])
    return prog
