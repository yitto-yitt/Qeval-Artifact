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
    
    for i in range(cycles):
        circuit.append(cirq.ry(e)(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f'm_{i}'))
            
    final_key = f'm_{cycles}' if bomb_live else 'm_0'
    circuit.append(cirq.measure(q, key=final_key))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        final_measurements = result.measurements[final_key].flatten()
        intermediate_measurements = np.column_stack([
            result.measurements[f'm_{i}'].flatten() for i in range(cycles)
        ])
        
        for r in range(shots):
            if final_measurements[r] == 1:
                detonations += 1
            elif np.any(intermediate_measurements[r] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_measurements = result.measurements[final_key].flatten()
        for r in range(shots):
            if final_measurements[r] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
