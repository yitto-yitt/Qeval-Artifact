# EVAL_META: task_id=68, framework=qpanda2, class=1
from numpy import pi
from pyqpanda import init_qvm, finalize_qvm, qAlloc_many, cAlloc_many, QProg, RY, Measure, run_with_configuration

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    init_qvm()
    q = qAlloc_many(1)
    c = cAlloc_many(measurements)
    prog = QProg()

    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])

    prog << Measure(q[0], c[measurements - 1])
    counts = run_with_configuration(prog, c, shots)
    finalize_qvm()

    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
