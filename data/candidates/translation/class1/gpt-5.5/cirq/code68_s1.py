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
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f"m{i}"))

    final_key = f"m{cycles}" if bomb_live else "m0"
    circuit.append(cirq.measure(q, key=final_key))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        for r in range(shots):
            final_measurement = int(result.measurements[f"m{cycles}"][r][0])
            prior_measurements = [int(result.measurements[f"m{i}"][r][0]) for i in range(cycles)]

            if final_measurement == 1:
                detonations += 1
            elif any(prior_measurements):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        measurements = result.measurements["m0"][:, 0]
        live_predictions = int((measurements == 0).sum())
        dud_predictions = int((measurements == 1).sum())
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
