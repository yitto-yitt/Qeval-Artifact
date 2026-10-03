# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = pi / cycles

    if bomb_live:
        kraus = []
        for s in (0, 1):
            for f in (0, 1):
                k = np.zeros((4, 4), dtype=complex)
                inp = 2 * s + f
                out = 2 * s + (f or s)
                k[out, inp] = 1.0
                kraus.append(k)

        dev = qml.device("default.mixed", wires=2)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
                qml.QubitChannel(kraus, wires=[0, 1])
            return qml.probs(wires=[0, 1])

        probs = circuit()
        live_predictions = float(probs[0])
        dud_predictions = float(probs[1])
        detonations = float(probs[2] + probs[3])
    else:
        dev = qml.device("default.qubit", wires=1)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.probs(wires=0)

        probs = circuit()
        live_predictions = float(probs[0])
        dud_predictions = float(probs[1])
        detonations = 0.0

    return {
        "live_predictions": live_predictions,
        "dud_predictions": dud_predictions,
        "detonations": detonations,
    }
