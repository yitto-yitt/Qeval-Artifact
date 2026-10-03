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
            circuit.append(cirq.Ry(rads=e).on(qubit))
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
        circuit.append(cirq.measure(qubit, key='final'))
    else:
        circuit.append(cirq.Ry(rads=e).on(qubit))
        for _ in range(1, cycles):
            circuit.append(cirq.Ry(rads=e).on(qubit))
        circuit.append(cirq.measure(qubit, key='final'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        for i in range(shots):
            final = result.measurements['final'][i][0]
            inter = any(result.measurements[f'm{j}'][i][0] == 1 for j in range(cycles))
            if final == 1:
                detonations += 1
            elif inter:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for i in range(shots):
            final = result.measurements['final'][i][0]
            if final == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
