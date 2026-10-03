# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
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
                samples.append(qml.sample(qml.PauliZ(0)))
            return tuple(samples)

        results = circuit()
        # results is tuple of arrays, each of shape (shots,); values in {+1,-1}
        # convert to bit: +1 -> 0, -1 -> 1
        import numpy as np
        arrs = [np.atleast_1d(r) for r in results]
        stacked = np.stack(arrs, axis=1)  # shape (shots, cycles)
        bits = (stacked == -1).astype(int)

        live_predictions = dud_predictions = detonations = 0
        for row in bits:
            # final measurement is last cycle's measurement
            if row[-1] == 1:
                detonations += 1
            elif any(row[:-1] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.PauliZ(0))

        import numpy as np
        res = np.atleast_1d(circuit())
        bits = (res == -1).astype(int)
        live_predictions = int((bits == 0).sum())
        dud_predictions = int((bits == 1).sum())
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
