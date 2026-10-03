# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    qvm = CPUQVM()
    qvm.init_qvm()

    cal_q = qvm.qAlloc_many(2)
    cal_c = qvm.cAlloc_many(2)
    cal_prog = QProg()
    cal_prog << X(cal_q[0]) << Measure(cal_q[0], cal_c[0]) << Measure(cal_q[1], cal_c[1])
    cal_res = qvm.run_with_configuration(cal_prog, cal_c, 1)
    cal_key = next(iter(cal_res))
    cal_bits = ''.join(ch for ch in str(cal_key) if ch in '01')
    c0_is_msb = cal_bits[0] == '1'

    live_predictions = dud_predictions = detonations = 0

    if bomb_live:
        n_meas = cycles + 1
        q = qvm.qAlloc_many(1)
        c = qvm.cAlloc_many(n_meas)
        prog = QProg()

        for i in range(cycles):
            prog << RY(q[0], e)
            prog << Measure(q[0], c[i])
        prog << Measure(q[0], c[cycles])

        res = qvm.run_with_configuration(prog, c, shots)

        for key, val in res.items():
            bits = ''.join(ch for ch in str(key) if ch in '01')
            if c0_is_msb:
                final_bit = bits[-1]
                other_bits = bits[:-1]
            else:
                final_bit = bits[0]
                other_bits = bits[1:]

            if final_bit == '1':
                detonations += val
            elif '1' in other_bits:
                dud_predictions += val
            else:
                live_predictions += val
    else:
        q = qvm.qAlloc_many(1)
        c = qvm.cAlloc_many(1)
        prog = QProg()

        for _ in range(cycles):
            prog << RY(q[0], e)
        prog << Measure(q[0], c[0])

        res = qvm.run_with_configuration(prog, c, shots)

        counts = {}
        for key, val in res.items():
            bits = ''.join(ch for ch in str(key) if ch in '01')
            counts[bits] = counts.get(bits, 0) + val

        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0

    qvm.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
