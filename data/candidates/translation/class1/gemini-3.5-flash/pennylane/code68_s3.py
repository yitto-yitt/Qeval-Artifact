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
            meas = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                meas.append(qml.measure(0))
            meas.append(qml.measure(0))
            return [qml.sample(m) for m in meas]
            
        samples = circuit()
        samples_matrix = np.array(samples).T
        
        detonations = 0
        dud_predictions = 0
        live_predictions = 0
        
        for shot in range(shots):
            final_meas = samples_matrix[shot][-1]
            mid_meas = samples_matrix[shot][:-1]
            if final_meas == 1:
                detonations += 1
            elif 1 in mid_meas:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.measure(0))
            
        samples = circuit()
        live_predictions = np.sum(samples == 0)
        dud_predictions = np.sum(samples == 1)
        detonations = 0
        
    return {
        "live_predictions": float(live_predictions / shots),
        "dud_predictions": float(dud_predictions / shots),
        "detonations": float(detonations / shots),
    }
