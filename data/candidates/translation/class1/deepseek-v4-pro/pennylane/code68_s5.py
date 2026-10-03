# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    theta = np.pi / cycles
    ancilla_wires = list(range(1, cycles + 2))

    dev = qml.device(
        "default.qubit",
        wires=1 + cycles + 1,
        shots=shots,
        mcm_method="one-shot",
    )

    @qml.qnode(dev)
    def circuit():
        for i in range(cycles):
            qml.RY(theta, wires=0)
            if bomb_live:
                m = qml.measure(wires=0)
                qml.cond(m, qml.PauliX)(wires=1 + i)

        if bomb_live:
            m_final = qml.measure(wires=0)
            qml.cond(m_final, qml.PauliX)(wires=1 + cycles)
            return qml.counts(wires=ancilla_wires)
        else:
            return qml.counts(wires=[0])

    counts = circuit()

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        for key, value in counts.items():
            if key == '0':
                live_predictions += value
            else:
                dud_predictions += value

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
