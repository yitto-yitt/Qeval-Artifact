# EVAL_META: task_id=68, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    device = qml.device("default.qubit", wires=1)

    @qml.set_shots(shots=shots)
    @qml.qnode(device, mcm_method="one-shot")
    def circuit():
        history = []
        for _ in range(cycles):
            qml.RY(np.pi / cycles, wires=0)
            if bomb_live:
                history.append(qml.measure(0))
        return tuple(qml.sample(m) for m in history) + (qml.sample(wires=0),)

    samples = circuit()
    final = np.asarray(samples[-1]).reshape(-1)

    if bomb_live:
        history = np.column_stack(
            [np.asarray(sample).reshape(-1) for sample in samples[:-1]]
        )
        prior_one = np.any(history == 1, axis=1)
        detonations = np.count_nonzero(final == 1)
        dud_predictions = np.count_nonzero((final == 0) & prior_one)
        live_predictions = np.count_nonzero((final == 0) & ~prior_one)
    else:
        live_predictions = np.count_nonzero(final == 0)
        dud_predictions = np.count_nonzero(final == 1)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
