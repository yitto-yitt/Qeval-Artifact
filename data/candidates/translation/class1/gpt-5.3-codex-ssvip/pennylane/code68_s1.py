# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    if bomb_live:
        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        p_survive = 1.0
        p_zero = 1.0
        p_one = 0.0

        for i in range(cycles):
            dev = qml.device("default.qubit", wires=1, shots=shots)

            @qml.qnode(dev)
            def step_circuit():
                qml.RY(e, wires=0)
                return qml.probs(wires=0)

            probs = step_circuit()
            p0_step = float(probs[0])
            p1_step = float(probs[1])

            det_this = p_survive * p1_step
            detonations += int(round(det_this * shots))

            p_survive *= p0_step
            p_zero = 1.0
            p_one = 0.0

        live_predictions += int(round(p_survive * shots))
        dud_predictions += shots - live_predictions - detonations

    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def full_circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.probs(wires=0)

        probs = full_circuit()
        live_predictions = int(round(float(probs[0]) * shots))
        dud_predictions = shots - live_predictions
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
