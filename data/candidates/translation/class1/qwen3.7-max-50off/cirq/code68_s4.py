# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    measurements = cycles + 1 if bomb_live else 1
    
    for i in range(cycles):
        circuit.append(cirq.Ry(rads=e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f'm{i}'))
            
    circuit.append(cirq.measure(q, key=f'm{measurements - 1}'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        last_meas = result.measurements[f'm{cycles}'][:, 0]
        
        inter_meas = np.zeros((shots, cycles), dtype=bool)
        for i in range(cycles):
            inter_meas[:, i] = result.measurements[f'm{i}'][:, 0]
            
        any_inter = np.any(inter_meas, axis=1)
        
        detonations = int(np.sum(last_meas == 1))
        dud_predictions = int(np.sum((last_meas == 0) & any_inter))
        live_predictions = int(np.sum((last_meas == 0) & ~any_inter))
    else:
        meas = result.measurements['m0'][:, 0]
        live_predictions = int(np.sum(meas == 0))
        dud_predictions = int(np.sum(meas == 1))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
