# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    
    dev = qml.device("default.qubit", shots=shots)
    
    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            ms = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                ms.append(qml.measure(0))
            final_m = qml.measure(0)
            ms.append(final_m)
            return tuple(qml.sample(m) for m in ms)
        
        results = circuit()
        res_array = np.array(results).astype(int)
        
        live_predictions = 0
        dud_predictions = 0
        detonations = 0
        
        for s in range(shots):
            final_val = res_array[cycles, s]
            intermediate_vals = res_array[:cycles, s]
            
            if final_val == 1:
                detonations += 1
            elif np.any(intermediate_vals == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
                
    else:
        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.measure(0))
            
        results = np.array(circuit()).astype(int)
        live_predictions = int(np.sum(results == 0))
        dud_predictions = int(np.sum(results == 1))
        detonations = 0

    return {
        "live_predictions": float(live_predictions / shots),
        "dud_predictions": float(dud_predictions / shots),
        "detonations": float(detonations / shots),
    }
