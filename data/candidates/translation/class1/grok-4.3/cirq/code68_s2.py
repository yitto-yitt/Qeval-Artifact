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
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        for shot in range(shots):
            exploded = any(result.measurements[f'm{i}'][shot][0] == 1 for i in range(cycles))
            if exploded:
                detonations += 1
            else:
                final_val = result.measurements['final'][shot][0]
                if final_val == 0:
                    live_predictions += 1
                else:
                    dud_predictions += 1
    else:
        finals = result.measurements['final'][:, 0]
        live_predictions = int(sum(finals == 0))
        dud_predictions = int(sum(finals == 1))
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
