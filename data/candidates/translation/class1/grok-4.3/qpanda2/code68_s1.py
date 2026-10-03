# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi/cycles
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc(1)
    measurements = cycles + 1 if bomb_live else 1
    c = qvm.cAlloc(measurements)
    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    prog << Measure(q[0], c[measurements - 1])
    counts = qvm.run_with_configuration(prog, shots)
    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1'] if '1' in counts else 0
        detonations = 0
    qvm.finalize()
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
