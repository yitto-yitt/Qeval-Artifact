# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
    circuit.append(cirq.measure(qubit, key='final'))

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        for rep in range(shots):
            detonated = False
            dud = False
            for i in range(cycles):
                val = result.measurements[f'm{i}'][rep][0]
                if val == 1:
                    detonated = True
                    break
                elif val == 0 and i > 0:
                    # Actually check if any earlier measurement was 1
                    pass
            if not detonated:
                # Check if any intermediate measurement was 1
                for i in range(cycles):
                    if result.measurements[f'm{i}'][rep][0] == 1:
                        dud = True
                        break
                if dud:
                    dud_predictions += 1
                else:
                    # No detonation and no intermediate 1
                    final_val = result.measurements['final'][rep][0]
                    if final_val == 0:
                        live_predictions += 1
                    else:
                        dud_predictions += 1
            else:
                detonations += 1
    else:
        final_counts = result.measurements['final']
        for rep in range(shots):
            val = final_counts[rep][0]
            if val == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
