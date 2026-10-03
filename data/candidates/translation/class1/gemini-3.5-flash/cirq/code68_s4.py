# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
            circuit.append(cirq.measure(q, key=f'm_{i}'))
        circuit.append(cirq.measure(q, key=f'm_{cycles}'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
        circuit.append(cirq.measure(q, key=f'm_{cycles}'))
        
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        counts = {}
        for s in range(shots):
            key = "".join(str(result.measurements[f'm_{i}'][s][0]) for i in reversed(range(cycles + 1)))
            counts[key] = counts.get(key, 0) + 1
            
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        final_measurements = result.measurements[f'm_{cycles}'].flatten()
        live_predictions = np.sum(final_measurements == 0)
        dud_predictions = np.sum(final_measurements == 1)
        detonations = 0
        
    return {
        "live_predictions": float(live_predictions) / shots,
        "dud_predictions": float(dud_predictions) / shots,
        "detonations": float(detonations) / shots,
    }
