# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    if not bomb_live:
        dev = qml.device("default.qubit", wires=1, shots=shots)
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.measure(0))
        samples = circuit()
        counts = np.bincount(samples, minlength=2)
        live_predictions = counts[0] / shots
        dud_predictions = counts[1] / shots
        detonations = 0.0
        return {
            "live_predictions": live_predictions,
            "dud_predictions": dud_predictions,
            "detonations": detonations,
        }
    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)
        @qml.qnode(dev)
        def circuit():
            ms = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                ms.append(qml.measure(0))
            ms.append(qml.measure(0))
            return [qml.sample(m) for m in ms]
        all_samples = circuit()
        live_predictions = dud_predictions = detonations = 0
        for shot in range(shots):
            final = all_samples[-1][shot]
            inter = [all_samples[i][shot] for i in range(cycles)]
            if final == 1:
                detonations += 1
            elif any(x == 1 for x in inter):
                dud_predictions += 1
            else:
                live_predictions += 1
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
