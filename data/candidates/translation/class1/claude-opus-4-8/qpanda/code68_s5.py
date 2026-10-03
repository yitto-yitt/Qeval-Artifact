# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, RY, measure
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    machine = CPUQVM()
    qubits = range(1)
    cbits = range(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(0, e)
        if bomb_live:
            prog << measure(0, i)
    prog << measure(0, measurements - 1)

    machine.run(prog, shots)
    raw_counts = machine.result().get_counts()

    counts = {}
    for key, value in raw_counts.items():
        norm = key.zfill(measurements)
        counts[norm] = counts.get(norm, 0) + value

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
