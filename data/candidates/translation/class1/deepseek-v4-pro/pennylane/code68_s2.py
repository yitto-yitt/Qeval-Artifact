# EVAL_META: task_id=68, framework=pennylane, class=1
import math
import numpy as np
import pennylane as qml


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    theta = math.pi / cycles

    if bomb_live:
        dev = qml.device("default.qubit", wires=cycles + 1, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(theta, wires=0)
                m = qml.measure(0)
                qml.cond(m, qml.PauliX)(wires=i + 1)
            return qml.sample(wires=list(range(1, cycles + 1)))

        samples = circuit()
        last = samples[:, -1]
        earlier = samples[:, :-1]

        detonations = int(np.sum(last == 1))
        dud_predictions = int(np.sum((last == 0) & np.any(earlier == 1, axis=1)))
        live_predictions = int(np.sum(np.all(samples == 0, axis=1)))

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }

    dev = qml.device("default.qubit", wires=1, shots=shots)

    @qml.qnode(dev)
    def circuit():
        for _ in range(cycles):
            qml.RY(theta, wires=0)
        return qml.sample(wires=0)

    samples = np.asarray(circuit()).flatten()
    dud_predictions = int(np.sum(samples == 1))
    live_predictions = int(np.sum(samples == 0))

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": 0.0,
    }
