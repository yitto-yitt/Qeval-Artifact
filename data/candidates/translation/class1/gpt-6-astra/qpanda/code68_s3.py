# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import CPUQVM, QProg, RY, measure


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    measurements = cycles + 1 if bomb_live else 1
    program = QProg()

    for i in range(cycles):
        program << RY(0, pi / cycles)
        if bomb_live:
            program << measure(0, i)
    program << measure(0, measurements - 1)

    simulator = CPUQVM()
    simulator.run(program, shots)
    counts = simulator.result().get_counts()

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for key, count in counts.items():
            if key[0] == "1":
                detonations += count
            elif "1" in key[1:]:
                dud_predictions += count
            else:
                live_predictions += count
    else:
        live_predictions = counts.get("0", 0)
        dud_predictions = counts.get("1", 0)

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
