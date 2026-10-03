# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    dev = qml.device("default.qubit", shots=shots)
    
    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            m_results = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                m_results.append(qml.measure(0))
            m_results.append(qml.measure(0))
            return [qml.sample(m) for m in m_results]
        
        samples = circuit()
        samples_matrix = np.array(samples).T
        
        live_predictions = 0
        dud_predictions = 0
        detonations = 0
        
        for shot in samples_matrix:
            c_25 = shot[25]
            prev = shot[:25]
            if c_25 == 1:
                detonations += 1
            elif 1 in prev:
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
        live_predictions = int(np.sum(samples == 0))
        dud_predictions = int(np.sum(samples == 1))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
