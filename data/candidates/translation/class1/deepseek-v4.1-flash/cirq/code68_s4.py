# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
        circuit.append(cirq.measure(qubit, key='final'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
        circuit.append(cirq.measure(qubit, key='final'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        final_meas = result.measurements['final']
        for shot in range(shots):
            if final_meas[shot] == 1:
                detonations += 1
            else:
                any_intermediate_1 = False
                for i in range(cycles):
                    if result.measurements[f'm{i}'][shot] == 1:
                        any_intermediate_1 = True
                        break
                if any_intermediate_1:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        final_meas = result.measurements['final']
        for shot in range(shots):
            if final_meas[shot] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
