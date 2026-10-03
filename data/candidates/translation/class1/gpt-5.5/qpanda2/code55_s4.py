# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    calib_machine = CPUQVM()
    calib_machine.init_qvm()
    pos_of_cbit = [0, 1, 2]

    for j in range(3):
        q = calib_machine.qAlloc_many(3)
        c = calib_machine.cAlloc_many(3)
        calib_prog = QProg()
        for k in range(3):
            if k == j:
                calib_prog << X(q[k])
            calib_prog << Measure(q[k], c[k])
        calib_counts = calib_machine.run_with_configuration(calib_prog, c, 1)
        calib_key = next(iter(calib_counts.keys()))
        pos = calib_key.find("1")
        if pos >= 0:
            pos_of_cbit[j] = pos

    calib_machine.finalize()
    pos_to_cbit = {pos: idx for idx, pos in enumerate(pos_of_cbit)}

    machine = CPUQVM()
    machine.init_qvm()

    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    measure = machine.cAlloc_many(3)

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
        desired_pos = 2 - i
        cidx = pos_to_cbit.get(desired_pos, desired_pos)
        prog << Measure(ancillary[i], measure[cidx])

    shots = 1024
    counts = machine.run_with_configuration(prog, measure, shots)
    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    machine.finalize()
    return result
