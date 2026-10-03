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
            measurements = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                measurements.append(qml.measure(0))
            measurements.append(qml.measure(0))
            return [qml.sample(m) for m in measurements]
            
        samples = circuit()
        samples = np.stack(samples, axis=1)
        
        detonations = 0
        dud_predictions = 0
        live_predictions = 0
        
        for sample in samples:
            if sample[-1] == 1:
                detonations += 1
            elif np.any(sample[:-1] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit_false():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)
            
        samples = circuit_false()
        live_predictions = np.sum(samples == 0)
        dud_predictions = np.sum(samples == 1)
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
