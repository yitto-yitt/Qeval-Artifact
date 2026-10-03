# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def circuit(bomb_live):
        ms = []
        for i in range(cycles):
            qml.RY(e, wires=0)
            if bomb_live:
                m = qml.measure(0)
                ms.append(m)
        m_final = qml.measure(0)
        ms.append(m_final)
        return tuple(ms)
    
    results = circuit(bomb_live)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        num_measurements = len(results)
        for shot in range(shots):
            qiskit_key = ''.join(str(int(results[j][shot])) for j in reversed(range(num_measurements)))
            if qiskit_key[0] == '1':
                detonations += 1
            elif '1' in qiskit_key[1:]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for shot in range(shots):
            outcome = results[0][shot]
            if outcome == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
