# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    ancilla = n

    prog = pq.QProg()
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

    shots = 1
    result = machine.run_with_configuration(prog, c, shots)

    bitstrings = list(result.keys())
    machine.finalize()
    return [bitstrings, result]
