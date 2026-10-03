# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    for i in range(cycles):
        circuit.append(cirq.ry(e)(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f"m{i}"))

    circuit.append(cirq.measure(q, key="final"))

    simulator = cirq.Simulator(seed=42, dtype=np.complex128)
    result = simulator.run(circuit, repetitions=shots)

    final_bits = result.measurements["final"][:, 0]

    if bomb_live:
        intermediate_bits = np.column_stack(
            [result.measurements[f"m{i}"][:, 0] for i in range(cycles)]
        )
        any_intermediate_one = np.any(intermediate_bits == 1, axis=1)

        detonations = int(np.count_nonzero(final_bits == 1))
        dud_predictions = int(np.count_nonzero((final_bits == 0) & any_intermediate_one))
        live_predictions = int(np.count_nonzero((final_bits == 0) & ~any_intermediate_one))
    else:
        live_predictions = int(np.count_nonzero(final_bits == 0))
        dud_predictions = int(np.count_nonzero(final_bits == 1))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
