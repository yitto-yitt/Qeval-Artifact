# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(q))
            circuit.append(cirq.measure(q, key=f'm{i}'))
        circuit.append(cirq.measure(q, key='final'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(q))
        circuit.append(cirq.measure(q, key='final'))

    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=shots)

    if bomb_live:
        finals = result.measurements['final'][:, 0]
        ms = [result.measurements[f'm{i}'][:, 0] for i in range(cycles)]
        for s in range(shots):
            if finals[s] == 1:
                detonations += 1
            else:
                if any(ms[i][s] == 1 for i in range(cycles)):
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        finals = result.measurements['final'][:, 0]
        for b in finals:
            if b == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
