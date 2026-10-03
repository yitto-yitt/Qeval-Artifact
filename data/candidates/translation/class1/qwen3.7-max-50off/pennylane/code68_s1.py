# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    if bomb_live:
        dev = qml.device("default.qubit", shots=shots)
        
        @qml.qnode(dev)
        def circuit():
            m_ids = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                m_ids.append(qml.measure(0))
            final_m = qml.measure(0)
            return [qml.sample(m) for m in m_ids] + [qml.sample(final_m)]
        
        res = circuit()
        results = np.array(res).T
        
        live_predictions = 0
        dud_predictions = 0
        detonations = 0
        
        for row in results:
            final_meas = row[-1]
            intermediate_meas = row[:-1]
            
            if final_meas == 1:
                detonations += 1
            elif 1 in intermediate_meas:
                dud_predictions += 1
            else:
                live_predictions += 1
                
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
    else:
        dev = qml.device("default.qubit", shots=shots)
        
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)
            
        results = circuit()
        live_predictions = int(np.sum(results == 0))
        dud_predictions = int(np.sum(results == 1))
        detonations = 0
        
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
