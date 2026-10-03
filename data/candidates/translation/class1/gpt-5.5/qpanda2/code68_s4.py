# EVAL_META: task_id=68, framework=qpanda2, class=1
from math import pi
from pyqpanda import CPUQVM, QProg, RY, Measure, X


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    prog << Measure(q[0], c[measurements - 1])

    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        bit_positions = []
        for idx in range(measurements):
            cal_qvm = CPUQVM()
            cal_qvm.init_qvm()
            cal_q = cal_qvm.qAlloc_many(measurements)
            cal_c = cal_qvm.cAlloc_many(measurements)
            cal_prog = QProg()
            cal_prog << X(cal_q[idx])
            for j in range(measurements):
                cal_prog << Measure(cal_q[j], cal_c[j])
            cal_counts = cal_qvm.run_with_configuration(cal_prog, cal_c, 1)
            cal_qvm.finalize()
            cal_key = next(iter(cal_counts.keys()))
            cal_bits = "".join(ch for ch in cal_key if ch in "01")
            bit_positions.append(cal_bits.find("1"))

        final_pos = bit_positions[measurements - 1]
        intermediate_positions = [bit_positions[i] for i in range(cycles)]

        for key, value in counts.items():
            bits = "".join(ch for ch in key if ch in "01")
            if bits[final_pos] == "1":
                detonations += value
            elif any(bits[pos] == "1" for pos in intermediate_positions):
                dud_predictions += value
            else:
                live_predictions += value
    else:
        for key, value in counts.items():
            bits = "".join(ch for ch in key if ch in "01")
            if bits[0] == "0":
                live_predictions += value
            else:
                dud_predictions += value
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
