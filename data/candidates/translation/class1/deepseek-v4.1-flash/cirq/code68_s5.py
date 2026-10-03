# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    e = np.pi / cycles
    shots = 1024
    qubit = cirq.LineQubit(0)
    simulator = cirq.Simulator()
    
    if bomb_live:
        circuit = cirq.Circuit()
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
        circuit.append(cirq.measure(qubit, key='final'))
        results = simulator.run(circuit, repetitions=shots)
        
        final = results.measurements['final'][:, 0]
        intermediates = np.array([results.measurements[f'm{i}'][:, 0] for i in range(cycles)])
        any_intermediate = np.any(intermediates == 1, axis=0)
        
        detonations = np.sum(final == 1)
        dud_predictions = np.sum((final == 0) & any_intermediate)
        live_predictions = np.sum((final == 0) & (~any_intermediate))
    else:
        circuit = cirq.Circuit()
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
        circuit.append(cirq.measure(qubit, key='final'))
        results = simulator.run(circuit, repetitions=shots)
        
        final = results.measurements['final'][:, 0]
        live_predictions = np.sum(final == 0)
        dud_predictions = np.sum(final == 1)
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
