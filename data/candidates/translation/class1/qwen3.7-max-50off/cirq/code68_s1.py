# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    keys = []
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            key = f'm_{i}'
            circuit.append(cirq.measure(qubit, key=key))
            keys.append(key)
            
    final_key = f'm_{cycles}'
    circuit.append(cirq.measure(qubit, key=final_key))
    keys.append(final_key)
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        final_meas = result.measurements[final_key].flatten()
        inter_meas = [result.measurements[f'm_{i}'].flatten() for i in range(cycles)]
        
        for s in range(shots):
            is_final_1 = final_meas[s] == 1
            is_any_inter_1 = any(inter_meas[i][s] == 1 for i in range(cycles))
            
            if is_final_1:
                detonations += 1
            elif is_any_inter_1:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_meas = result.measurements[final_key].flatten()
        for s in range(shots):
            if final_meas[s] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
                
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
