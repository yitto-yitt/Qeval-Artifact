# EVAL_META: task_id=68, framework=qiskit, class=1
import math


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = math.pi / (2 * cycles)

    if bomb_live:
        live_prediction_probability = math.cos(theta) ** (2 * cycles)
        detonation_probability = 1.0 - live_prediction_probability
        dud_prediction_probability = 0.0
    else:
        live_prediction_probability = 0.0
        dud_prediction_probability = 1.0
        detonation_probability = 0.0

    return {
        "live_predictions": live_prediction_probability,
        "dud_predictions": dud_prediction_probability,
        "detonations": detonation_probability,
    }
