# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    if bomb_live:
        dev = qml.device("default.qubit", wires=1, shots=shots)
        @qml.qnode(dev)
        def circuit():
            results = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                results.append(qml.measure(0))
            results.append(qml.measure(0))
            return tuple(qml.sample(r) for r in results)
        samples = circuit()
        live_predictions = dud_predictions = detonations = 0
        for shot in range(shots):
            final = samples[-1][shot]
            inters = [samples[i][shot] for i in range(cycles)]
            if final == 1:
                detonations += 1
            elif any(x == 1 for x in inters):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)
        @qml.qnode(dev)
        def circuit():
            qml.RY(np.pi, wires=0)
            return qml.sample(qml.measure(0))
        samples = circuit()
        live_predictions = np.sum(samples == 0)
        dud_predictions = np.sum(samples == 1)
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
