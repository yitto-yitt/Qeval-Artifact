# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=1)

    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            results = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                results.append(qml.measure(0))
            return [qml.sample(m) for m in results]

        live_predictions = dud_predictions = detonations = 0
        for _ in range(shots):
            outcomes = circuit()
            outcomes = [int(np.array(o)) for o in outcomes]
            final = outcomes[-1]
            if final == 1:
                detonations += 1
            elif 1 in outcomes[:-1]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.PauliZ(0))

        live_predictions = dud_predictions = detonations = 0
        for _ in range(shots):
            z = int(np.array(circuit()))
            bit = 0 if z == 1 else 1
            if bit == 0:
                live_predictions += 1
            else:
                dud_predictions += 1

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
