# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = pi / cycles

    if bomb_live:
        k0 = np.zeros((4, 4), dtype=complex)
        k0[0, 0] = 1.0
        k0[1, 1] = 1.0

        k10 = np.zeros((4, 4), dtype=complex)
        k10[3, 2] = 1.0

        k11 = np.zeros((4, 4), dtype=complex)
        k11[3, 3] = 1.0

        dev = qml.device("default.mixed", wires=2)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
                qml.QubitChannel([k0, k10, k11], wires=[0, 1])
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
