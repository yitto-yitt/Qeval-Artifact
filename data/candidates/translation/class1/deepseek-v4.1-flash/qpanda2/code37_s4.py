# EVAL_META: task_id=37, framework=qpanda2, class=1
import builtins
from pyqpanda import *


def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)

    prog = QProg()
    prog << X(qubits[n])
    for i in range(n + 1):
        prog << H(qubits[i])
    for index, bit in enumerate(reversed(s)):
        if bit == '1':
            prog << CNOT(qubits[index], qubits[n])
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n):
        prog << Measure(qubits[i], cbits[i])

    result = qvm.run_with_configuration(prog, cbits, 1)

    key = list(result.keys())[0]
    if isinstance(key, str):
        bitstring = key.zfill(n)
    else:
        bitstring = bin(key)[2:].zfill(n)
    bitstring = bitstring[::-1]
    bitstrings = [bitstring]

    return [bitstrings, result]
