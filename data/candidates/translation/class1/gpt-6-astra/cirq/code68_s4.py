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
    final_one = result.measurements["final"][:, 0] == 1

    if bomb_live:
        earlier_one = np.any(
            np.column_stack([
                result.measurements[f"cycle_{i}"][:, 0]
                for i in range(cycles)
            ]),
            axis=1,
        )
        detonations = np.count_nonzero(final_one)
        dud_predictions = np.count_nonzero(~final_one & earlier_one)
        live_predictions = np.count_nonzero(~final_one & ~earlier_one)
    else:
        detonations = 0
        dud_predictions = np.count_nonzero(final_one)
        live_predictions = np.count_nonzero(~final_one)

    return {
        "live_predictions": float(live_predictions / shots),
        "dud_predictions": float(dud_predictions / shots),
        "detonations": float(detonations / shots),
    }
