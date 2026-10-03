# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def circuit_live():
        m_values = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            m_values.append(qml.measure(0))
        m_values.append(qml.measure(0))
        return [qml.sample(m) for m in m_values]

    @qml.qnode(dev)
    def circuit_dud():
        for i in range(cycles):
            qml.RY(e, wires=0)
        return qml.sample(wires=0)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        samples = circuit_live()
        samples = np.stack(samples, axis=1)
        for i in range(shots):
            last_meas = samples[i, -1]
            prev_meas = samples[i, :-1]
            if last_meas == 1:
                detonations += 1
            elif np.any(prev_meas == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        samples = circuit_dud()
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
