# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *

def or_gate(a, b):
    init(QMachineType.CPU)

    cal_q = qAlloc_many(3)
    cal_c = cAlloc_many(3)
    cal_prog = QProg()
    cal_prog << X(cal_q[0])
    cal_prog << Measure(cal_q[0], cal_c[0])
    cal_prog << Measure(cal_q[1], cal_c[1])
    cal_prog << Measure(cal_q[2], cal_c[2])
    cal_counts = run_with_configuration(cal_prog, cal_c, 1)
    c0_is_left = next(iter(cal_counts))[0] == '1'

    q_a = qAlloc_many(3)
    q_b = qAlloc_many(3)
    anc = qAlloc_many(3)
    meas = cAlloc_many(3)
    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(q_a[i])
        if b_bits[2 - i] == '0':
            prog << X(q_b[i])

    for i in range(3):
        prog << Toffoli(q_a[i], q_b[i], anc[i])
        prog << X(anc[i])

    if c0_is_left:
        prog << Measure(anc[2], meas[0])
        prog << Measure(anc[1], meas[1])
        prog << Measure(anc[0], meas[2])
    else:
        prog << Measure(anc[2], meas[2])
        prog << Measure(anc[1], meas[1])
        prog << Measure(anc[0], meas[0])

    shots = 1024
    counts = run_with_configuration(prog, meas, shots)
    finalize()

    return {key: value / shots for key, value in counts.items()}
