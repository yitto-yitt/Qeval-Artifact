# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    if bomb_live:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
                qml.measure(wires=0, reset=True)
            return qml.sample(wires=0)

        final_samples = circuit()
        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bit in final_samples:
            if int(bit) == 1:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        final_samples = circuit()
        live_predictions = int((final_samples == 0).sum())
        dud_predictions = int((final_samples == 1).sum())
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
