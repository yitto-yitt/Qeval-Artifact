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
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
    
    circuit.append(cirq.measure(qubit, key=f'm{measurements - 1}'))
    
    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        for i in range(shots):
            # Get measurement results for this shot
            result_bits = []
            for j in range(measurements):
                result_bits.append(results.measurements[f'm{j}'][i][0])
            
            # Check if first measurement was 1 (detonation)
            if result_bits[0] == 1:
                detonations += 1
            # Check if any subsequent measurement was 1 (dud prediction)
            elif 1 in result_bits[1:]:
                dud_predictions += 1
            # Otherwise it's a live prediction
            else:
                live_predictions += 1
    else:
        # For dud bomb case, we only have one measurement at the end
        for i in range(shots):
            if results.measurements[f'm{measurements - 1}'][i][0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        
        # No detonations possible with dud bomb
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
