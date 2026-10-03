# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles

    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(q))
            circuit.append(cirq.measure(q, key=f"m{i}"))
        circuit.append(cirq.measure(q, key=f"m{cycles}"))
    else:
        for _ in range(cycles):
            circuit.append(cirq.ry(e).on(q))
        circuit.append(cirq.measure(q, key="m0"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        for r in range(shots):
            bits = [int(result.measurements[f"m{i}"][r, 0]) for i in range(cycles + 1)]
            if bits[0] == 1:
                detonations += 1
            elif any(b == 1 for b in bits[1:]):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        vals = result.measurements["m0"][:, 0]
        live_predictions = int(np.sum(vals == 0))
        dud_predictions = int(np.sum(vals == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
