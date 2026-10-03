# EVAL_META: task_id=37, framework=qpanda2, class=1
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
            prog << pq.Measure(q[i], c[i])

        raw_counts = qvm.run_with_configuration(prog, c, shots)
    finally:
        qvm.finalize()

    reverse_keys = False
    if n > 1:
        cal_qvm = pq.CPUQVM()
        cal_qvm.init_qvm()
        try:
            cq = cal_qvm.qAlloc_many(2)
            cc = cal_qvm.cAlloc_many(2)
            cal_prog = pq.QProg()
            cal_prog << pq.X(cq[0])
            cal_prog << pq.Measure(cq[0], cc[0])
            cal_prog << pq.Measure(cq[1], cc[1])
            cal_counts = cal_qvm.run_with_configuration(cal_prog, cc, 1)
            cal_key = next(iter(cal_counts.keys()))
            reverse_keys = cal_key == "10"
        finally:
            cal_qvm.finalize()

    result = {}
    for key, count in raw_counts.items():
        out_key = key[::-1] if reverse_keys else key
        result[out_key] = result.get(out_key, 0) + int(count)

    bitstrings = []
    for key, count in result.items():
        bitstrings.extend([key] * int(count))

    return [bitstrings, result]
