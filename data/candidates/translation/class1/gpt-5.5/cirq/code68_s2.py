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

    for i in range(cycles):
        circuit.append(cirq.ry(e)(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f"m{i}"))

    final_key = f"m{cycles}" if bomb_live else "m0"
    circuit.append(cirq.measure(q, key=final_key))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        final_measurements = result.measurements[f"m{cycles}"][:, 0]
        intermediate_measurements = [
            result.measurements[f"m{i}"][:, 0] for i in range(cycles)
        ]

        for shot in range(shots):
            if final_measurements[shot] == 1:
                detonations += 1
            elif any(measurements[shot] == 1 for measurements in intermediate_measurements):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_measurements = result.measurements["m0"][:, 0]
        live_predictions = int((final_measurements == 0).sum())
        dud_predictions = int((final_measurements == 1).sum())
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
