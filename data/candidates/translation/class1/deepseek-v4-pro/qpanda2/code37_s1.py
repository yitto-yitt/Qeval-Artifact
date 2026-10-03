# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *

def bv_algorithm(s):
    n = len(s)
    init(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.allocateQubits(n + 1)
    c = qvm.allocateCBits(n)
    prog = QProg()
    ancilla = n

    prog << X(q[ancilla])
    for i in range(n + 1):
        prog << H(q[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << Measure(q[i], c[i])

    shots = 1
    result = qvm.run_with_configuration(prog, c, shots)
    bitstrings = list(result.keys())
    return [bitstrings, result]
