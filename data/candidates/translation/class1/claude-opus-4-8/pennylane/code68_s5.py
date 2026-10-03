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
        @qml.qnode(dev)
        def circuit():
            samples = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                samples.append(qml.sample(wires=0))
            return qml.sample(wires=0)

        # We need per-cycle measurement collapse. Use mid-circuit measurements.
        @qml.qnode(dev)
        def circuit_mcm():
            outcomes = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                m = qml.measure(0)
                outcomes.append(m)
            return [qml.sample(o) for o in outcomes]

        results = circuit_mcm()
        results = np.array(results)  # shape (cycles, shots)

        live_predictions = dud_predictions = detonations = 0
        for s in range(shots):
            col = results[:, s]
            if col[-1] == 1:
                detonations += 1
            elif np.any(col[:-1] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit_dud():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        samples = np.array(circuit_dud())
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
