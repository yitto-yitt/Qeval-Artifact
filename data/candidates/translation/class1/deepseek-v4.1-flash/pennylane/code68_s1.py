# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = np.pi / cycles
    shots = 1024
    
    dev = qml.device('default.qubit', wires=1, shots=shots)
    
    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            ms = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                ms.append(qml.measure(0))
            ms.append(qml.measure(0))
            return qml.sample(ms)
        
        results = circuit()
        live_predictions = 0
        dud_predictions = 0
        detonations = 0
        for row in results:
            if row[-1] == 1:
                detonations += 1
            elif 1 in row[:-1]:
                dud_predictions += 1
            else:
                live_predictions += 1
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            m = qml.measure(0)
            return qml.sample(m)
        
        results = circuit()
        live_predictions = np.sum(results == 0)
        dud_predictions = np.sum(results == 1)
        detonations = 0
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
