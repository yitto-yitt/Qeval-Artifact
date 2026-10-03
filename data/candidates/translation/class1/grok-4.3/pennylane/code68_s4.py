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
                mid_measurements.append(qml.measure(0))
        final_measurement = qml.measure(0)
        if bomb_live:
            return [qml.sample(m) for m in mid_measurements + [final_measurement]]
        else:
            return qml.sample(final_measurement)
    results = circuit()
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        all_samples = np.array(results).T
        finals = all_samples[:, -1]
        mids = all_samples[:, :-1]
        for final, mid in zip(finals, mids):
            if final == 1:
                detonations += 1
            elif np.any(mid == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        counts_0 = np.sum(results == 0)
        counts_1 = np.sum(results == 1)
        live_predictions = counts_0
        dud_predictions = counts_1
        detonations = 0
    total = shots
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
