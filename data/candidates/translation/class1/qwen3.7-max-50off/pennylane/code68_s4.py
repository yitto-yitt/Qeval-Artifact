# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    
    dev = qml.device("default.qubit", shots=shots)
    
    @qml.qnode(dev)
    def circuit():
        m_list = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                m_list.append(qml.measure(0))
        m_list.append(qml.measure(0))
        return [qml.sample(m) for m in m_list]
    
    res = circuit()
    if isinstance(res, tuple) or isinstance(res, list):
        outcomes = np.stack(res, axis=1)
    else:
        outcomes = np.array(res)
        if outcomes.ndim == 1:
            outcomes = outcomes.reshape(-1, 1)
            
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        last_meas = outcomes[:, -1]
        other_meas = outcomes[:, :-1]
        
        for i in range(shots):
            if last_meas[i] == 1:
                detonations += 1
            elif np.any(other_meas[i] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for i in range(shots):
            if outcomes[i, 0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
                
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
