# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)

    prog = pq.QProg()

    prog << pq.X(q[n])

    for i in range(n + 1):
        prog << pq.H(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[n])

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(n):
        prog << pq.Measure(q[i], c[i])

    result = machine.run_with_configuration(prog, c, 1)
    bitstrings = list(result.keys())

    return [bitstrings, result]
