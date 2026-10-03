# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, CNOT, measure


def bv_algorithm(s):
    n = len(s)
    ancilla = n

    qc = QCircuit()
    qc << X(ancilla)
    for i in range(n + 1):
        qc << H(i)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(index, ancilla)
    for i in range(n):
        qc << H(i)

    prog = QProg()
    prog << qc
    for i in range(n):
        prog << measure(i, i)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    result = qvm.result()
    counts = result.get_counts()

    bitstrings = []
    for key, cnt in counts.items():
        bitstrings.extend([key] * cnt)

    return [bitstrings, result]
