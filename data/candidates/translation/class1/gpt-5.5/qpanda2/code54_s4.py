# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    shots = 1024

    cal_q = qvm.qAlloc_many(3)
    cal_c = qvm.cAlloc_many(3)
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)

    cal_prog = QProg()
    cal_prog.insert(X(cal_q[0]))
    for i in range(3):
        cal_prog.insert(Measure(cal_q[i], cal_c[i]))
    cal_counts = qvm.run_with_configuration(cal_prog, cal_c, 1)
    cal_key = max(cal_counts, key=cal_counts.get)
    reverse_keys = len(cal_key) == 3 and cal_key[0] == "1"

    qr_a = q[0:3]
    qr_b = q[3:6]
    ancillary = q[6:9]

    prog = QProg()
    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            prog.insert(X(qr_a[i]))
        if b_bits[2 - i] == "1":
            prog.insert(X(qr_b[i]))

    for i in range(3):
        prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))

    for i in range(3):
        prog.insert(Measure(ancillary[i], c[i]))

    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())

    processed = {}
    for key, value in counts.items():
        out_key = key[::-1] if reverse_keys else key
        processed[out_key] = processed.get(out_key, 0) + value

    qvm.finalize()
    return {key: value / total for key, value in processed.items()}
