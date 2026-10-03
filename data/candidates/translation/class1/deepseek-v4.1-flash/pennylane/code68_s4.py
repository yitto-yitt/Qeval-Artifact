# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    if bomb_live:
        measurements = cycles + 1
        
        @qml.qnode(dev)
        def circuit():
            ms = []
            for _ in range(cycles):
                qml.RY(e, wires=0)
                m = qml.measure(0)
                ms.append(m)
            m_final = qml.measure(0)
            ms.append(m_final)
            return tuple(qml.sample(m) for m in ms)
        
        results = circuit()
        outcomes = np.array(results).astype(int)
        
        final = outcomes[cycles, :]
        intermediate = outcomes[:cycles, :]
        
        detonations = np.sum(final == 1)
        final_zero = (final == 0)
        any_intermediate_one = np.any(intermediate == 1, axis=0)
        dud_mask = final_zero & any_intermediate_one
        live_mask = final_zero & (~any_intermediate_one)
        
        dud_predictions = np.sum(dud_mask)
        live_predictions = np.sum(live_mask)
        
        return {
            "live_predictions": float(live_predictions) / shots,
            "dud_predictions": float(dud_predictions) / shots,
            "detonations": float(detonations) / shots,
        }
    else:
        @qml.qnode(dev)
        def circuit():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            m = qml.measure(0)
            return qml.sample(m)
        
        results = circuit().astype(int)
        live_predictions = np.sum(results == 0)
        dud_predictions = np.sum(results == 1)
        detonations = 0
        
        return {
            "live_predictions": float(live_predictions) / shots,
            "dud_predictions": float(dud_predictions) / shots,
            "detonations": float(detonations) / shots,
        }
