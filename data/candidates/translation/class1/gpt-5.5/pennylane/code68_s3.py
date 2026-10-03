# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots, seed=12345)

    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            measurements = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                measurements.append(qml.measure(0))
            return tuple(qml.sample(m) for m in measurements)

        results = circuit()
        samples = np.stack([np.asarray(r, dtype=int).reshape(-1) for r in results], axis=1)
        final_measurement = samples[:, -1]

        detonations = int(np.sum(final_measurement == 1))
        dud_predictions = int(np.sum((final_measurement == 0) & np.any(samples == 1, axis=1)))
        live_predictions = int(np.sum((final_measurement == 0) & ~np.any(samples == 1, axis=1)))
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        samples = np.asarray(circuit(), dtype=int).reshape(-1)
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
