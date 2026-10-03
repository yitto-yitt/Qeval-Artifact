# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / N
    if bomb_live:
        cos_val = np.cos(theta / 2)
        p_survive = cos_val ** (2 * N)
        p_live = p_survive
        p_dud = 0.0
        p_det = 1.0 - p_survive
    else:
        p_live = 0.0
        p_dud = 1.0
        p_det = 0.0
    return {
        'live_predictions': p_live,
        'dud_predictions': p_dud,
        'detonations': p_det
    }
