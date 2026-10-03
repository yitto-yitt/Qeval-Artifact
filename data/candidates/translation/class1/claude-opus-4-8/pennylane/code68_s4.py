# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots)

    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            outcomes = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                outcomes.append(qml.sample(wires=0))
            return qml.sample(wires=0)

        samples = circuit()
        samples = np.array(samples)  # shape (cycles, shots)

        live_predictions = dud_predictions = detonations = 0
        for s in range(shots):
            col = samples[:, s]
            last = col[-1]
            earlier = col[:-1]
            if last == 1:
                detonations += 1
            elif np.any(earlier == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        samples = np.array(circuit())
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
