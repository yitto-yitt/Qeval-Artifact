# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    dev = qml.device("default.qubit", wires=1, shots=shots)
    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            mcms = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                m = qml.measure(wires=0)
                mcms.append(m)
            m_final = qml.measure(wires=0)
            mcms.append(m_final)
            return [qml.sample(m) for m in mcms]
        samples = circuit()
        live_predictions = dud_predictions = detonations = 0
        num_mcms = len(samples)
        for s in range(shots):
            final = samples[-1][s]
            inter_has_1 = any(samples[i][s] == 1 for i in range(num_mcms - 1))
            if final == 1:
                detonations += 1
            elif inter_has_1:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)
        samples = circuit()
        live_predictions = np.sum(samples == 0)
        dud_predictions = np.sum(samples == 1)
        detonations = 0
    total = shots
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
