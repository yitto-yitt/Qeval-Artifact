# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

pq.init(pq.QMachineType.CPU)

def not_gate(a):
    a_bin = format(a, "08b")
    q = pq.qAlloc_many(8)
    c = pq.cAlloc_many(8)
    prog = pq.QProg()

    for i in range(8):
        if a_bin[7 - i] == "0":
            prog << pq.X(q[i])

    prog << pq.MeasureAll(q, c)
    counts = pq.run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
