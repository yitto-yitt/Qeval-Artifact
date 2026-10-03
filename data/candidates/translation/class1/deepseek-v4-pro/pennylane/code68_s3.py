# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    theta = np.pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots)

    @qml.qnode(dev)
    def circuit():
        mid_measurements = []
        for _ in range(cycles):
            qml.RY(theta, wires=0)
            if bomb_live:
                mid_measurements.append(qml.measure(0))
        if bomb_live:
            return tuple([qml.sample(m) for m in mid_measurements] + [qml.sample(wires=0)])
        return qml.sample(wires=0)

    if bomb_live:
        samples = circuit()
        intermediate = np.array(samples[:-1])
        final = np.array(samples[-1])

        live_predictions = int(np.sum((final == 0) & np.all(intermediate == 0, axis=0)))
        dud_predictions = int(np.sum((final == 0) & np.any(intermediate == 1, axis=0)))
        detonations = int(np.sum(final == 1))

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }

    final = np.array(circuit())
    live_predictions = int(np.sum(final == 0))
    dud_predictions = int(np.sum(final == 1))
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": 0.0,
    }
