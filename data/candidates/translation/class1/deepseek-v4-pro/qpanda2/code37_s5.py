# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(n + 1)
    c = pq.cAlloc_many(n)
    prog = pq.QProg()
    ancilla = n

    prog << pq.X(q[ancilla])
    for i in range(n + 1):
        prog << pq.H(q[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[ancilla])
    for i in range(n):
        prog << pq.H(q[i])
    for i in range(n):
        prog << pq.Measure(q[i], c[i])

    cbits_out = [c[i] for i in range(n - 1, -1, -1)]
    result = pq.run_with_configuration(prog, cbits_out, 1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
