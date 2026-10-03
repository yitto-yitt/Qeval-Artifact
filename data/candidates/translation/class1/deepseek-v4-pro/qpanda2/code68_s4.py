# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(1)
    c = cAlloc_many(measurements)
    prog = QProg()

    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])

    prog << Measure(q[0], c[measurements - 1])

    counts = run_with_configuration(prog, c, shots)

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

    destroy_quantum_machine()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
