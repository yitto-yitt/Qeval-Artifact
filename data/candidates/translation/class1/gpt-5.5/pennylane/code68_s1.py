# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots)

    if bomb_live:
        @qml.qnode(dev, mcm_method="one-shot")
        def circuit():
            measurements = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                measurements.append(qml.measure(0))
            return tuple(qml.sample(m) for m in measurements) + (qml.sample(wires=0),)

        result = circuit()
        samples = [np.asarray(r).reshape(-1).astype(int) for r in result]
        mid_samples = np.stack(samples[:-1], axis=1)
        final_samples = samples[-1]

        detonation_mask = final_samples == 1
        dud_mask = (final_samples == 0) & np.any(mid_samples == 1, axis=1)
        live_mask = (final_samples == 0) & ~np.any(mid_samples == 1, axis=1)

        live_predictions = int(np.sum(live_mask))
        dud_predictions = int(np.sum(dud_mask))
        detonations = int(np.sum(detonation_mask))
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        samples = np.asarray(circuit()).reshape(-1).astype(int)
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
