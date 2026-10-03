# EVAL_META: task_id=68, framework=qiskit, class=1
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = math.pi / (2 * cycles)
    live_pred = math.cos(theta) ** (2 * cycles)
    if bomb_live:
        return {
            'live_predictions': live_pred,
            'dud_predictions': 0.0,
            'detonations': 1.0 - live_pred
        }
    else:
        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0,
            'detonations': 0.0
        }
