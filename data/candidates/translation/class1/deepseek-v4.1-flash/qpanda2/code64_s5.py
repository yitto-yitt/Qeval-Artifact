# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2 * n)
    cbits = qvm.cAlloc_many(n)

    prog = QProg()

    # Hadamard on first register
    for i in range(n):
        prog << H(qubits[i])

    prog << BARRIER(qubits)

    # CNOT between reg1[i] -> reg2[i]
    for i in range(n):
        prog << CNOT(qubits[i], qubits[n + i])

    # If there is a '1' in s (after reversal), apply the coupling and H on reg1
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                prog << CNOT(qubits[i], qubits[n + j])
        prog << BARRIER(qubits)
        for k in range(n):
            prog << H(qubits[k])

    # Measure reg1 into the classical register 'c'
    for k in range(n):
        prog << Measure(qubits[k], cbits[k])

    return prog
