# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    for i in range(cycles):
        circuit.append(cirq.ry(e)(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
    circuit.append(cirq.measure(qubit, key='final'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for rep in range(shots):
            detonated = False
            dud = False
            for i in range(cycles):
                if result.measurements[f'm{i}'][rep][0] == 1:
                    detonated = True
                    break
                elif result.measurements[f'm{i}'][rep][0] == 0:
                    pass
            if not detonated:
                if result.measurements['final'][rep][0] == 1:
                    dud = True
            if detonated:
                detonations += 1
            elif dud:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_meas = result.measurements['final']
        for rep in range(shots):
            if final_meas[rep][0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
