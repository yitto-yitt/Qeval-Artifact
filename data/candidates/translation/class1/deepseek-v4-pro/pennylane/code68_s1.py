# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles

    if bomb_live:
        first_flag = 1
        later_flag = 2
        dev = qml.device("default.qubit", wires=3, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
                m_probe = qml.measure(0)
                if i == 0:
                    qml.cond(m_probe == 1, qml.PauliX)(first_flag)
                else:
                    m_flag = qml.measure(later_flag)
                    qml.cond((m_flag == 0) & (m_probe == 1), qml.PauliX)(later_flag)
            return qml.sample(wires=[first_flag, later_flag])

        samples = circuit()
        first_samples = samples[:, 0]
        later_samples = samples[:, 1]
        detonations = int(np.sum(first_samples == 1))
        dud_predictions = int(np.sum((first_samples == 0) & (later_samples == 1)))
        live_predictions = int(np.sum((first_samples == 0) & (later_samples == 0)))
    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=[0])

        samples = circuit()
        if samples.ndim > 1:
            samples = samples[:, 0]
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
