# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def play_circuit():
        results = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                results.append(qml.measure(0))
        results.append(qml.measure(0))
        return [qml.sample(op) for op in results]
        
    samples = play_circuit()
    if not isinstance(samples, tuple):
        samples = np.array([samples]).T
    else:
        samples = np.stack(samples, axis=1)
        
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        for row in samples:
            if row[-1] == 1:
                detonations += 1
            elif 1 in row[:-1]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for row in samples:
            if row[0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
