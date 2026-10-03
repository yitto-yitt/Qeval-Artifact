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
        measurements = []
        for _ in range(cycles):
            qml.RY(np.pi / cycles, wires=0)
            if bomb_live:
                measurements.append(qml.measure(0))
        return tuple(qml.sample(m) for m in measurements) + (
            qml.sample(wires=0),
        )

    samples = np.column_stack(
        [np.asarray(result).reshape(-1) for result in circuit()]
    )
    final_one = samples[:, -1] == 1

    if bomb_live:
        previous_one = np.any(samples[:, :-1] == 1, axis=1)
        live_predictions = np.count_nonzero(~final_one & ~previous_one)
        dud_predictions = np.count_nonzero(~final_one & previous_one)
        detonations = np.count_nonzero(final_one)
    else:
        live_predictions = np.count_nonzero(~final_one)
        dud_predictions = np.count_nonzero(final_one)
        detonations = 0

    return {
        "live_predictions": float(live_predictions / shots),
        "dud_predictions": float(dud_predictions / shots),
        "detonations": float(detonations / shots),
    }
