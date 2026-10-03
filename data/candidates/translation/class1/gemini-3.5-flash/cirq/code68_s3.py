# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
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
        circuit.append(cirq.measure(q, key='m_0'))
        
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        last_meas = result.measurements[f'm_{cycles}'].flatten()
        inter_meas = [result.measurements[f'm_{i}'].flatten() for i in range(cycles)]
        any_inter_1 = np.any(np.stack(inter_meas, axis=0) == 1, axis=0)
        
        detonations = int(np.sum(last_meas == 1))
        dud_predictions = int(np.sum((last_meas != 1) & any_inter_1))
        live_predictions = int(np.sum((last_meas != 1) & ~any_inter_1))
    else:
        meas = result.measurements['m_0'].flatten()
        live_predictions = int(np.sum(meas == 0))
        dud_predictions = int(np.sum(meas == 1))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
