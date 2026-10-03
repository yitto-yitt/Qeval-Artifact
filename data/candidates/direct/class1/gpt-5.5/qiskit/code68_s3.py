# EVAL_META: task_id=68, framework=qiskit, class=1

import math


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = math.pi / (2 * cycles)

    if bool(bomb_live):
        live_predictions = math.cos(theta) ** (2 * cycles)
        dud_predictions = 0.0
        detonations = 1.0 - live_predictions
    else:
        live_predictions = 0.0
        dud_predictions = 1.0
        detonations = 0.0

    return {
        "live_predictions": float(live_predictions),
        "dud_predictions": float(dud_predictions),
        "detonations": float(detonations),
    }
