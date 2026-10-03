# EVAL_META: task_id=68, framework=qiskit, class=1

import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    """
    Simulates the Zeno Elitzur-Vaidman bomb tester routine using 25 cycles.
    Returns the probabilities of successful live-bomb predictions, dud-bomb predictions, and detonations.
    """
    N = 25
    theta = np.pi / N
    
    if bomb_live:
        p_live = np.cos(theta / 2) ** (2 * N)
        p_det = 1.0 - p_live
        p_dud = 0.0
    else:
        p_live = 0.0
        p_det = 0.0
        p_dud = 1.0
        
    return {
        'live_predictions': float(p_live),
        'dud_predictions': float(p_dud),
        'detonations': float(p_det)
    }
