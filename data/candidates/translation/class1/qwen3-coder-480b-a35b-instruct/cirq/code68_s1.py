# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    qubit = cirq.LineQubit(0)
    
    circuit = cirq.Circuit()
    
    measurements = []
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            measurement = cirq.NamedQubit(f'measure_{i}')
            circuit.append(cirq.measure(qubit, key=f'meas_{i}'))
            measurements.append(f'meas_{i}')
    
    # Final measurement
    final_measurement_key = 'final_meas'
    circuit.append(cirq.measure(qubit, key=final_measurement_key))
    
    # Run simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        # For live bomb, we check all measurements
        for i in range(shots):
            # If first measurement is 1, it detonates
            if result.measurements[measurements[0]][i] == 1:
                detonations += 1
            else:
                # Check if any subsequent measurement is 1 (dud prediction)
                is_dud = False
                for j in range(1, len(measurements)):
                    if result.measurements[measurements[j]][i] == 1:
                        dud_predictions += 1
                        is_dud = True
                        break
                # If no measurement was 1, it's a live prediction
                if not is_dud:
                    final_result = result.measurements[final_measurement_key][i]
                    if final_result == 0:
                        live_predictions += 1
    else:
        # For dud bomb, only final measurement matters
        final_results = result.measurements[final_measurement_key]
        dud_predictions = np.sum(final_results)
        live_predictions = shots - dud_predictions
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
