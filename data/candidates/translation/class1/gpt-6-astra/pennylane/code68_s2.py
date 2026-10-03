# EVAL_META: task_id=68, framework=pennylane, class=1
import numpy as np
import pennylane as qml


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    device = qml.device("default.qubit", wires=1)

    @qml.set_shots(shots)
    @qml.qnode(device, mcm_method="one-shot")
    def circuit():
        measurements = []
        for _ in range(cycles):
            qml.RY(np.pi / cycles, wires=0)
            if bomb_live:
                measurements.append(qml.measure(0))
        if bomb_live:
            return tuple(qml.sample(m) for m in measurements) + (
                qml.sample(wires=0),
            )
        return qml.sample(wires=0)

    samples = circuit()
    if bomb_live:
        history = np.stack(
            [np.asarray(sample).reshape(-1) for sample in samples[:-1]]
        )
        final = np.asarray(samples[-1]).reshape(-1)
        previous_one = np.any(history == 1, axis=0)
        live_predictions = np.count_nonzero((final == 0) & ~previous_one)
        dud_predictions = np.count_nonzero((final == 0) & previous_one)
        detonations = np.count_nonzero(final == 1)
    else:
        final = np.asarray(samples).reshape(-1)
        live_predictions = np.count_nonzero(final == 0)
        dud_predictions = np.count_nonzero(final == 1)
        detonations = 0

    return {
        "live_predictions": float(live_predictions / shots),
        "dud_predictions": float(dud_predictions / shots),
        "detonations": float(detonations / shots),
    }
