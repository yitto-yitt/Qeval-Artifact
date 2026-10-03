# EVAL_META: task_id=68, framework=qiskit, class=1
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = math.pi / (2 * N)
    survival = math.cos(theta) ** (2 * N)
    if bomb_live:
        return {
            'live_predictions': survival,
            'dud_predictions': 0.0,
            'detonations': 1.0 - survival
        }
    return {
        'live_predictions': 0.0,
        'dud_predictions': 1.0,
        'detonations': 0.0
    }
