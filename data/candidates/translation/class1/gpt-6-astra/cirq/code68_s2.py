# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    for i in range(cycles):
        circuit.append(cirq.ry(np.pi / cycles)(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f"cycle_{i}"))
    circuit.append(cirq.measure(qubit, key="final"))

    result = cirq.Simulator().run(circuit, repetitions=shots)
    final = result.measurements["final"][:, 0].astype(bool)

    if bomb_live:
        prior_one = np.any(
            np.column_stack([
                result.measurements[f"cycle_{i}"][:, 0]
                for i in range(cycles)
            ]),
            axis=1,
        )
        detonations = int(np.count_nonzero(final))
        dud_predictions = int(np.count_nonzero(~final & prior_one))
        live_predictions = int(np.count_nonzero(~final & ~prior_one))
    else:
        live_predictions = int(np.count_nonzero(~final))
        dud_predictions = int(np.count_nonzero(final))
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
