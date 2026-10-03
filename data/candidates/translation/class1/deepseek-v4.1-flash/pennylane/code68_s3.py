# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = pi / cycles
    shots = 1024
    measurements = cycles + 1 if bomb_live else 1
    
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def circuit():
        outcomes = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                m = qml.measure(0)
                outcomes.append(m)
        m_final = qml.measure(0)
        outcomes.append(m_final)
        return outcomes
    
    results = circuit()
    samples = np.array(results).T
    
    if bomb_live:
        final_bits = samples[:, -1]
        intermediate_bits = samples[:, :-1]
        detonations = np.sum(final_bits == 1)
        any_intermediate_1 = np.any(intermediate_bits == 1, axis=1)
        dud_predictions = np.sum((final_bits == 0) & any_intermediate_1)
        live_predictions = np.sum((final_bits == 0) & (~any_intermediate_1))
    else:
        final_bits = samples[:, 0]
        live_predictions = np.sum(final_bits == 0)
        dud_predictions = np.sum(final_bits == 1)
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
