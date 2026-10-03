# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    
    dev = qml.device("default.qubit", shots=shots)
    
    @qml.qnode(dev)
    def circuit_live():
        ms = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            ms.append(qml.measure(0))
        return [qml.sample(m) for m in ms] + [qml.sample(wires=0)]

    @qml.qnode(dev)
    def circuit_dud():
        for i in range(cycles):
            qml.RY(e, wires=0)
        return qml.sample(wires=0)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        res = circuit_live()
        samples = np.column_stack(res)
        final_meas = samples[:, -1]
        mid_meas = samples[:, :-1]
        
        for i in range(shots):
            if final_meas[i] == 1:
                detonations += 1
            elif np.any(mid_meas[i] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        res = circuit_dud()
        for val in res:
            if val == 0:
                live_predictions += 1
            else:
                dud_predictions += 1

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
