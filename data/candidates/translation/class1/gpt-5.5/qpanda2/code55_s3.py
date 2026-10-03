# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    shots = 1024

    def _cbit_positions():
        positions = {}
        for idx in range(3):
            qvm_cal = CPUQVM()
            qvm_cal.init_qvm()
            qs = qvm_cal.qAlloc_many(3)
            cs = qvm_cal.cAlloc_many(3)
            prog_cal = QProg()
            prog_cal << X(qs[idx])
            for j in range(3):
                prog_cal << Measure(qs[j], cs[j])
            counts_cal = qvm_cal.run_with_configuration(prog_cal, cs, 1)
            qvm_cal.finalize()
            key = next(iter(counts_cal.keys()))
            positions[idx] = key.index("1")
        return positions

    pos = _cbit_positions()

    qvm = CPUQVM()
    qvm.init_qvm()

    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    measure = qvm.cAlloc_many(3)

    prog = QProg()

    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "0":
            prog << X(qr_a[i])
        if b[2 - i] == "0":
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], measure[i])

    counts = qvm.run_with_configuration(prog, measure, shots)
    qvm.finalize()

    remapped = {}
    for key, value in counts.items():
        out_key = key[pos[2]] + key[pos[1]] + key[pos[0]]
        remapped[out_key] = remapped.get(out_key, 0) + value

    total = builtins.sum(remapped.values())
    return {key: value / total for key, value in remapped.items()}
