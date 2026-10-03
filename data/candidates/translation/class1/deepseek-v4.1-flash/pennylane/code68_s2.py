# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = np.pi / cycles
    shots = 1024
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def circuit(bomb_live):
        measurements = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                m = qml.measure(0)
                measurements.append(m)
        m_final = qml.measure(0)
        measurements.append(m_final)
        return tuple(qml.sample(m) for m in measurements)
    
    samples = circuit(bomb_live)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        samples_array = np.array(samples).T
        for shot in samples_array:
            final = shot[-1]
            earlier = shot[:-1]
            if final == 1:
                detonations += 1
            elif np.any(earlier == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_samples = samples[0]
        for val in final_samples:
            if val == 1:
                dud_predictions += 1
            else:
                live_predictions += 1
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
