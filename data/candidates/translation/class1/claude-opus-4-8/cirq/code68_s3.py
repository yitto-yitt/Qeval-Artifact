# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f'm{i}'))
    circuit.append(cirq.measure(q, key='final'))
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=shots)
    if bomb_live:
        final = result.measurements['final'][:, 0]
        inter = np.stack([result.measurements[f'm{i}'][:, 0] for i in range(cycles)], axis=1)
        for s in range(shots):
            if final[s] == 1:
                detonations += 1
            elif inter[s].any():
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final = result.measurements['final'][:, 0]
        live_predictions = int((final == 0).sum())
        dud_predictions = int((final == 1).sum())
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
