# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
        circuit.append(cirq.measure(qubit, key=f'm{cycles}'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
        circuit.append(cirq.measure(qubit, key='m0'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        for shot in range(shots):
            final = result.measurements[f'm{cycles}'][shot]
            if final == 1:
                detonations += 1
            else:
                any_earlier = any(result.measurements[f'm{i}'][shot] == 1 for i in range(cycles))
                if any_earlier:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        for shot in range(shots):
            outcome = result.measurements['m0'][shot]
            if outcome == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
                
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
