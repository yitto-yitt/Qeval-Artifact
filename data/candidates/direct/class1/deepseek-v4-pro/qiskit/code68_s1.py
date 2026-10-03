# EVAL_META: task_id=68, framework=qiskit, class=1

import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    """
    Zeno Elitzur-Vaidman bomb tester with 25 cycles.
    Returns a distribution over possible outcomes for the given bomb condition.
    """
    N = 25
    theta = math.pi / (2 * N)
    
    if bomb_live:
        # Survival probability = cos^(2N)(theta) = cos^50(pi/50)
        survive_prob = math.cos(theta) ** (2 * N)
        det_prob = 1.0 - survive_prob
        return {'live_predictions': survive_prob,
                'dud_predictions': 0.0,
                'detonations': det_prob}
    else:
        # Dud bomb: always yields a dud prediction, never detonates.
        return {'live_predictions': 0.0,
                'dud_predictions': 1.0,
                'detonations': 0.0}
