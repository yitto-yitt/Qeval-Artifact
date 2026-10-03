# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    inter_keys = []
    for i in range(cycles):
        circuit.append(cirq.ry(e)(qubit))
        if bomb_live:
            k = f'inter{i}'
            circuit.append(cirq.measure(qubit, key=k))
            inter_keys.append(k)
    final_key = 'final'
    circuit.append(cirq.measure(qubit, key=final_key))
    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=shots)
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        final_bits = results.measurements[final_key].flatten()
        inter_bits_list = [results.measurements[k].flatten() for k in inter_keys]
        for s in range(shots):
            key_str = str(int(final_bits[s]))
            for j in range(cycles - 1, -1, -1):
                key_str += str(int(inter_bits_list[j][s]))
            if key_str[0] == '1':
                detonations += 1
            elif '1' in key_str[1:]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        final_bits = results.measurements[final_key].flatten()
        counts_0 = np.sum(final_bits == 0)
        counts_1 = np.sum(final_bits == 1)
        live_predictions = counts_0
        dud_predictions = counts_1
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
