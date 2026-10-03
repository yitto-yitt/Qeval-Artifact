# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    machine = CPUQVM()
    machine.initQVM()
    q = machine.qAlloc_many(1)[0]
    c = machine.cAlloc_many(measurements)
    prog = QProg()

    for i in range(cycles):
        prog << RY(q, e)
        if bomb_live:
            prog << Measure(q, c[i])
    prog << Measure(q, c[measurements - 1])

    if bomb_live:
        cbits = list(reversed(c))
    else:
        cbits = [c[0]]

    counts = machine.run_with_configuration(prog, cbits, shots)

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

    machine.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
