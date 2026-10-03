# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)

    bits = format(a, "08b")
    prog = pq.QProg()
    for i in range(8):
        if bits[7 - i] == "0":
            prog << pq.X(q[i])

    for i in range(8):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
