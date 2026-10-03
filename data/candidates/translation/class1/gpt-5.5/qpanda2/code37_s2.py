# EVAL_META: task_id=37, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    shots = 1

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        q = qvm.qAlloc_many(n + 1)
        c = qvm.cAlloc_many(n)

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
            prog << pq.Measure(q[n - 1 - i], c[i])

        result = qvm.run_with_configuration(prog, c, shots)

        bitstrings = []
        for bitstring, count in result.items():
            bitstrings.extend([bitstring] * int(count))

        return [bitstrings, result]
    finally:
        qvm.finalize()
