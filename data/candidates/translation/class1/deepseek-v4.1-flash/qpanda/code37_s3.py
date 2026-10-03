# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, H, X, CNOT, measure, CPUQVM


def bv_algorithm(s):
    n = len(s)
    prog = QProg()
    q = [Qubit(i) for i in range(n + 1)]
    c = [CBit(i) for i in range(n)]
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
        prog << measure(q[i], c[i])

    machine = CPUQVM()
    machine.run(prog, 1)
    result = machine.result()
    bitstrings = list(result.get_counts().keys())
    return [bitstrings, result]
