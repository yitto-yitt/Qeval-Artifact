# EVAL_META: task_id=68, framework=qiskit, class=1
import math


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = math.pi / (2 * cycles)

    if bomb_live:
        live_predictions = math.cos(theta) ** (2 * cycles)
        detonations = 1.0 - live_predictions
        dud_predictions = 0.0
    else:
        live_predictions = 0.0
        dud_predictions = 1.0
        detonations = 0.0

    return {
        "live_predictions": live_predictions,
        "dud_predictions": dud_predictions,
        "detonations": detonations,
    }
