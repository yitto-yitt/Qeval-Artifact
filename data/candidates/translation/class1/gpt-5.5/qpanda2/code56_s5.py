# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def not_gate(a):
    init(QMachineType.CPU)
    shots = 1024

    cal_q = qAlloc_many(8)
    cal_c = cAlloc_many(8)
    cal_prog = QProg()
    cal_prog << X(cal_q[0])
    for i in range(8):
        cal_prog << Measure(cal_q[i], cal_c[i])
    cal_counts = run_with_configuration(cal_prog, cal_c, shots)
    cal_key = next(iter(cal_counts.keys()))
    reverse_keys = (cal_key[0] == "1")

    q = qAlloc_many(8)
    c = cAlloc_many(8)
    prog = QProg()

    a_bits = format(a, "08b")
    for i in range(8):
        if a_bits[7 - i] == "0":
            prog << X(q[i])

    for i in range(8):
        prog << Measure(q[i], c[i])

    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {}
    for key, value in counts.items():
        out_key = key[::-1] if reverse_keys else key
        result[out_key] = value / total

    finalize()
    return result
