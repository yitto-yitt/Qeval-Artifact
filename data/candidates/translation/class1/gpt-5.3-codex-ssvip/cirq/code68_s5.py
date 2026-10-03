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

    for i in range(cycles):
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f"m{i}"))

    circuit.append(cirq.measure(q, key="final"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        final_bits = result.measurements["final"][:, 0]
        cycle_bits = np.column_stack([result.measurements[f"m{i}"][:, 0] for i in range(cycles)])

        for s in range(shots):
            if final_bits[s] == 1:
                detonations += 1
            elif np.any(cycle_bits[s, :] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_bits = result.measurements["final"][:, 0]
        live_predictions = int(np.sum(final_bits == 0))
        dud_predictions = int(np.sum(final_bits == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
