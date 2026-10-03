# EVAL_META: task_id=68, framework=cirq, class=1
import cirq

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = cirq.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(qubit))
        if bomb_live:
            circuit.append(cirq.measure(qubit, key=f'm{i}'))
    final_key = f'm{measurements-1}'
    circuit.append(cirq.measure(qubit, key=final_key))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    if bomb_live:
        meas_data = result.measurements
        for shot in range(shots):
            last_meas = meas_data[final_key][shot][0]
            any_inter = False
            for i in range(cycles):
                if meas_data[f'm{i}'][shot][0] == 1:
                    any_inter = True
                    break
            if last_meas == 1:
                detonations += 1
            elif any_inter:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        meas = result.measurements[final_key]
        for shot in range(shots):
            if meas[shot][0] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
