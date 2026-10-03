# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
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

    live_predictions = dud_predictions = detonations = 0
    finals = result.measurements['final'][:, 0]
    if bomb_live:
        inters = np.stack(
            [result.measurements[f'm{i}'][:, 0] for i in range(cycles)],
            axis=1,
        )
        for s in range(shots):
            if finals[s] == 1:
                detonations += 1
            elif inters[s].any():
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        detonations = 0
        dud_predictions = int(finals.sum())
        live_predictions = int((finals == 0).sum())

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
