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
            circuit.append(cirq.measure(q, key=f'm{i}'))
        circuit.append(cirq.measure(q, key=f'm{cycles}'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
        circuit.append(cirq.measure(q, key='m0'))
        
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        data = np.column_stack([result.measurements[f'm{i}'][:, 0] for i in range(cycles + 1)])
        final_vals = data[:, cycles]
        intermediate_any_one = np.any(data[:, :cycles] == 1, axis=1)
        
        detonations = np.sum(final_vals == 1)
        dud_predictions = np.sum((final_vals == 0) & intermediate_any_one)
        live_predictions = np.sum((final_vals == 0) & ~intermediate_any_one)
    else:
        m0_vals = result.measurements['m0'][:, 0]
        live_predictions = np.sum(m0_vals == 0)
        dud_predictions = np.sum(m0_vals == 1)
        detonations = 0
        
    return {
        "live_predictions": float(live_predictions) / shots,
        "dud_predictions": float(dud_predictions) / shots,
        "detonations": float(detonations) / shots,
    }
