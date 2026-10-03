# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f'm{i}'))
    circuit.append(cirq.measure(q, key='m_final'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    measurements = result.measurements
    
    final = measurements['m_final'].flatten()
    
    if bomb_live:
        inter_measurements = np.array([measurements[f'm{i}'].flatten() for i in range(cycles)])
        any_inter = np.any(inter_measurements == 1, axis=0)
        detonations = np.sum(final == 1)
        dud_predictions = np.sum((final == 0) & any_inter)
        live_predictions = np.sum((final == 0) & (~any_inter))
    else:
        live_predictions = np.sum(final == 0)
        dud_predictions = np.sum(final == 1)
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
