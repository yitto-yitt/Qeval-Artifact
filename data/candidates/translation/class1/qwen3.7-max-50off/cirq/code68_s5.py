# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    measurements = cycles + 1 if bomb_live else 1
    
    keys = []
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            key = f'm{i}'
            circuit.append(cirq.measure(qubit, key=key))
            keys.append(key)
            
    final_key = f'm{measurements - 1}'
    circuit.append(cirq.measure(qubit, key=final_key))
    keys.append(final_key)
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        last_meas = result.measurements[final_key][:, 0]
        earlier_meas = [result.measurements[k][:, 0] for k in keys[:-1]]
        
        for shot in range(shots):
            if last_meas[shot] == 1:
                detonations += 1
            elif any(m[shot] == 1 for m in earlier_meas):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        meas = result.measurements[final_key][:, 0]
        for shot in range(shots):
            if meas[shot] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
                
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
