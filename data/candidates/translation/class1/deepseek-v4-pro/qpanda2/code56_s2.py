# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def not_gate(a):
    pq.init(pq.QMachineType.CPU)
    q = pq.qAlloc_many(8)
    c = pq.cAlloc_many(8)
    prog = pq.QProg()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7 - i] == "0":
            prog << pq.X(q[i])
    for i in range(8):
        prog << pq.Measure(q[i], c[i])
    shots = 1024
    counts = pq.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
