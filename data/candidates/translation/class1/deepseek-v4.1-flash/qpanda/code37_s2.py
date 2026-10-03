# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure


def bv_algorithm(s):
    n = len(s)
    ancilla = n

    qvm = CPUQVM()
    qvm.init_qvm()

    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)

    prog = QProg()
    prog << X(qubits[ancilla])

    for i in range(n + 1):
        prog << H(qubits[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(qubits[index], qubits[ancilla])

    for i in range(n):
        prog << H(qubits[i])

    for i in range(n):
        prog << measure(qubits[i], cbits[i])

    result = qvm.run(prog, 1)

    if isinstance(result, dict):
        bitstrings = list(result.keys())
    else:
        counts = result.get_counts()
        bitstrings = list(counts.keys())

    return [bitstrings, result]
