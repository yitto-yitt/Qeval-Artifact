# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    dev = qml.device("default.qubit", wires=1, shots=shots)
    @qml.qnode(dev)
    def circuit():
        mid_measurements = []
        for _ in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                m = qml.measure(0)
                mid_measurements.append(qml.sample(m))
        m_final = qml.measure(0)
        mid_measurements.append(qml.sample(m_final))
        return tuple(mid_measurements)
    results = circuit()
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        num_mids = len(results) - 1
        for shot_idx in range(shots):
            final = results[-1][shot_idx]
            inters = [results[k][shot_idx] for k in range(num_mids)]
            if final == 1:
                detonations += 1
            elif any(x == 1 for x in inters):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        counts_0 = np.sum(results[0] == 0)
        counts_1 = np.sum(results[0] == 1)
        live_predictions = counts_0
        dud_predictions = counts_1
        detonations = 0
    total = shots
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
