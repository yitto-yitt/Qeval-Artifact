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
    intermediate_keys = []

    for i in range(cycles):
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            key = f"m{i}"
            intermediate_keys.append(key)
            circuit.append(cirq.measure(q, key=key))

    circuit.append(cirq.measure(q, key="final"))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        final_bits = result.measurements["final"][:, 0]
        intermediate_bits = [result.measurements[key][:, 0] for key in intermediate_keys]

        for shot in range(shots):
            if final_bits[shot] == 1:
                detonations += 1
            elif any(bits[shot] == 1 for bits in intermediate_bits):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_bits = result.measurements["final"][:, 0]
        live_predictions = int((final_bits == 0).sum())
        dud_predictions = int((final_bits == 1).sum())
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
