# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots)

    @qml.qnode(dev, mcm_method="one-shot")
    def circuit():
        measurements = []
        for _ in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                measurements.append(qml.measure(0))

        if bomb_live:
            return tuple(qml.sample(m) for m in measurements) + (qml.sample(wires=0),)

        return qml.sample(wires=0)

    results = circuit()

    if bomb_live:
        columns = [np.asarray(result).reshape(-1) for result in results]
        samples = np.column_stack(columns)
        intermediate = samples[:, :cycles]
        final = samples[:, cycles]

        detonations = int(np.count_nonzero(final == 1))
        dud_predictions = int(np.count_nonzero((final == 0) & np.any(intermediate == 1, axis=1)))
        live_predictions = int(np.count_nonzero((final == 0) & ~np.any(intermediate == 1, axis=1)))
    else:
        samples = np.asarray(results).reshape(-1)
        live_predictions = int(np.count_nonzero(samples == 0))
        dud_predictions = int(np.count_nonzero(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
