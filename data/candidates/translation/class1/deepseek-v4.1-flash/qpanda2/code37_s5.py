# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *

def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)
    ancilla = n

    prog = QProg()
    prog << X(qubits[ancilla])
    for i in range(n + 1):
        prog << H(qubits[i])
    for index, bit in enumerate(reversed(s)):
        if bit == '1':
            prog << CNOT(qubits[index], qubits[ancilla])
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n):
        prog << measure(qubits[i], cbits[n - 1 - i])

    result = qvm.run_with_configuration(prog, cbits, 1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
