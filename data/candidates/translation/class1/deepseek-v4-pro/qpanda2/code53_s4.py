# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def xor_gate(a, b):
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(8)
    c = pq.cAlloc_many(8)
    prog = pq.QProg()

    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(q[i])
        if (b >> i) & 1:
            prog << pq.X(q[i])

    for i in range(8):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    c_reversed = [c[i] for i in range(7, -1, -1)]
    counts = pq.run_with_configuration(prog, c_reversed, shots)
    total = builtins.sum(counts.values())
    pq.finalize()

    return {key: value / total for key, value in counts.items()}
