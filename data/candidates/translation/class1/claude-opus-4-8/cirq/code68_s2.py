# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    live_predictions = dud_predictions = detonations = 0
    sim = cirq.Simulator()

    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
            circuit.append(cirq.measure(q, key=f'm{i}'))
        circuit.append(cirq.measure(q, key='final'))
        result = sim.run(circuit, repetitions=shots)
        for s in range(shots):
            final = result.measurements['final'][s][0]
            if final == 1:
                detonations += 1
            else:
                dud = False
                for i in range(cycles):
                    if result.measurements[f'm{i}'][s][0] == 1:
                        dud = True
                        break
                if dud:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
        circuit.append(cirq.measure(q, key='final'))
        result = sim.run(circuit, repetitions=shots)
        for s in range(shots):
            if result.measurements['final'][s][0] == 1:
                dud_predictions += 1
            else:
                live_predictions += 1

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
