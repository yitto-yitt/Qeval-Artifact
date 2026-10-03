# EVAL_META: task_id=68, framework=qiskit, class=1
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    if bomb_live:
        theta = math.pi / (2 * N)
        p_no_detonation = math.cos(theta) ** (2 * N)
        return {
            'live_predictions': p_no_detonation,
            'dud_predictions': 0.0,
            'detonations': 1.0 - p_no_detonation
        }
    else:
        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0,
            'detonations': 0.0
        }
