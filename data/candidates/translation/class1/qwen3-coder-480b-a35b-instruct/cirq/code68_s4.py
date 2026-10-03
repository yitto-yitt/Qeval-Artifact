# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    # Add rotation gates
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'm_{i}'))
    
    # Final measurement
    circuit.append(cirq.measure(qubit, key=f'm_{cycles}' if bomb_live else 'm_final'))
    
    # Simulate the circuit
    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=shots)
    
    if bomb_live:
        for i in range(shots):
            # Check if first measurement was '1' (detonation)
            if results.measurements[f'm_0'][i][0] == 1:
                detonations += 1
            else:
                # Check if any subsequent measurement was '1' (dud prediction)
                is_dud = False
                for j in range(1, cycles):
                    if results.measurements[f'm_{j}'][i][0] == 1:
                        is_dud = True
                        break
                if is_dud:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        for i in range(shots):
            if results.measurements['m_final'][i][0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
