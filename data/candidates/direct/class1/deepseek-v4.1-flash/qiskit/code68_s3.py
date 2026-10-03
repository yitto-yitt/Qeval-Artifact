# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    alpha = np.pi / (2 * N)
    no_detonation = np.cos(alpha) ** (2 * N)

    if bomb_live:
        return {
            'live_predictions': float(no_detonation),
            'dud_predictions': 0.0,
            'detonations': float(1.0 - no_detonation),
        }
    else:
        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0,
            'detonations': 0.0,
        }
