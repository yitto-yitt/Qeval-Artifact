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
            # Check if the first measurement is 1 (detonation)
            if results.measurements[f'm0'][i][0] == 1:
                detonations += 1
            else:
                # Check if any subsequent measurement is 1 (dud prediction)
                is_dud = False
                for j in range(1, cycles):
                    if results.measurements[f'm{j}'][i][0] == 1:
                        is_dud = True
                        break
                if is_dud:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        # For dud bomb, check the single measurement
        for i in range(shots):
            if results.measurements[f'm0'][i][0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
