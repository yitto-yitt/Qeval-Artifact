# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles

    if bomb_live:
        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for _ in range(shots):
            detonated = False
            dud = False
            for _ in range(cycles):
                dev = qml.device("default.qubit", wires=1, shots=1)

                @qml.qnode(dev)
                def step():
                    qml.RY(e, wires=0)
                    return qml.sample(qml.PauliZ(0))

                z_sample = int(step()[0])
                bit = 0 if z_sample == 1 else 1  # map Z eigenvalue to computational bit
                if bit == 1:
                    detonations += 1
                    detonated = True
                    break
            if not detonated:
                dev_final = qml.device("default.qubit", wires=1, shots=1)

                @qml.qnode(dev_final)
                def final_measure():
                    return qml.sample(qml.PauliZ(0))

                z_final = int(final_measure()[0])
                final_bit = 0 if z_final == 1 else 1
                if final_bit == 1:
                    dud = True

                if dud:
                    dud_predictions += 1
                else:
                    live_predictions += 1

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }

    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.PauliZ(0))

        samples = circuit()
        bits = np.where(samples == 1, 0, 1)
        live_predictions = int(np.sum(bits == 0))
        dud_predictions = int(np.sum(bits == 1))
        detonations = 0

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
