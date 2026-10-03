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
        return tuple(qml.sample(m) for m in measurements) + (
            qml.sample(wires=[0]),
        )

    samples = circuit()
    final_one = np.asarray(samples[-1]).reshape(-1) == 1

    if bomb_live:
        earlier_samples = np.stack(
            [np.asarray(sample).reshape(-1) for sample in samples[:-1]],
            axis=1,
        )
        earlier_one = np.any(earlier_samples == 1, axis=1)
        live_predictions = np.mean(~final_one & ~earlier_one)
        dud_predictions = np.mean(~final_one & earlier_one)
        detonations = np.mean(final_one)
    else:
        live_predictions = np.mean(~final_one)
        dud_predictions = np.mean(final_one)
        detonations = 0.0

    return {
        "live_predictions": float(live_predictions),
        "dud_predictions": float(dud_predictions),
        "detonations": float(detonations),
    }
