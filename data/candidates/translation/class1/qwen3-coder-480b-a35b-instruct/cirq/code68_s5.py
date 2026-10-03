# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    for i in range(cycles):
        circuit.append(cirq.ry(e)(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'meas_{i}'))
    
    circuit.append(cirq.measure(qubit, key=f'meas_{measurements - 1}'))
    
    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        for i in range(shots):
            # Get measurement results for this shot
            meas_values = [results.measurements[f'meas_{j}'][i][0] for j in range(measurements)]
            if meas_values[0] == 1:  # First measurement indicates detonation
                detonations += 1
            elif 1 in meas_values[1:]:  # Later measurements indicate dud prediction
                dud_predictions += 1
            else:  # No detections indicate live prediction
                live_predictions += 1
    else:
        for i in range(shots):
            meas_value = results.measurements[f'meas_0'][i][0]
            if meas_value == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
