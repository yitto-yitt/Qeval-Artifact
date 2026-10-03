# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    if not bomb_live:
        return {'live_predictions': 0.0, 'dud_predictions': 1.0, 'detonations': 0.0}
    else:
        p_survive = (np.cos(theta) ** 2) ** N
        return {'live_predictions': p_survive, 'dud_predictions': 0.0, 'detonations': 1.0 - p_survive}
