# EVAL_META: task_id=68, framework=qiskit, class=1
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    n_cycles = 25
    theta = math.pi / n_cycles

    # Probability that a live bomb survives all cycles without detonating.
    live_survival_prob = math.cos(theta / 2.0) ** (2 * n_cycles)

    if bomb_live:
        return {
            "live_predictions": live_survival_prob,
            "dud_predictions": 0.0,
            "detonations": 1.0 - live_survival_prob,
        }

    return {
        "live_predictions": 0.0,
        "dud_predictions": 1.0,
        "detonations": 0.0,
    }
