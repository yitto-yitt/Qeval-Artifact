# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    if bomb_live:
        meas_keys = []
        for i in range(cycles):
            circuit.append(cirq.Ry(rads=e).on(q))
            key = f'm{i}'
            circuit.append(cirq.measure(q, key=key))
            meas_keys.append(key)
        final_key = 'final'
        circuit.append(cirq.measure(q, key=final_key))
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=shots)
        live_predictions = dud_predictions = detonations = 0
        for shot in range(shots):
            final = result.measurements[final_key][shot][0]
            inter_has_1 = any(result.measurements[k][shot][0] == 1 for k in meas_keys)
            if final == 1:
                detonations += 1
            elif inter_has_1:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for i in range(cycles):
            circuit.append(cirq.Ry(rads=e).on(q))
        circuit.append(cirq.measure(q, key='final'))
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=shots)
        counts = result.histogram(key='final')
        live_predictions = counts.get(0, 0)
        dud_predictions = counts.get(1, 0)
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
