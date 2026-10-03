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
            m_list = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                m_list.append(qml.measure(0))
            m_list.append(qml.measure(0))
            return [qml.sample(m) for m in m_list]
            
        samples = np.array(circuit())
        
        live_predictions = 0
        dud_predictions = 0
        detonations = 0
        
        for shot in range(shots):
            final_val = samples[-1, shot]
            mid_vals = samples[:-1, shot]
            
            if final_val == 1:
                detonations += 1
            elif np.any(mid_vals == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit_dud():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            m = qml.measure(0)
            return qml.sample(m)
            
        samples = circuit_dud()
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
