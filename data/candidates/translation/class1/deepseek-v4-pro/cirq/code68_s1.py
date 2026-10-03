# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    shots = 1024
    e = np.pi / cycles

    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()

    if bomb_live:
        # intermediate measurement keys + final key
        keys = [cirq.MeasurementKey(f"m{i}") for i in range(cycles)]
        keys.append(cirq.MeasurementKey("final"))
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
            circuit.append(cirq.measure(qubit, key=keys[i]))
        # final measurement (no extra rotation)
        circuit.append(cirq.measure(qubit, key=keys[-1]))
        # run
        result = cirq.Simulator().run(circuit, repetitions=shots)
        # collect measurement data in the same order as keys
        data = [result.measurements[key.name] for key in keys]
        # stack into a (shots, cycles+1) array and convert to bitstrings
        stacked = np.column_stack(data)
        bitstrings = [''.join(str(b) for b in row) for row in stacked]

        # classification
        live = dud = det = 0
        for bs in bitstrings:
            if bs[0] == '1':
                det += 1
            elif '1' in bs[1:]:
                dud += 1
            else:
                live += 1
        return {
            "live_predictions": live / shots,
            "dud_predictions": dud / shots,
            "detonations": det / shots
        }
    else:
        # dud bomb – just apply all rotations and measure once
        for _ in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
        circuit.append(cirq.measure(qubit, key="final"))
        result = cirq.Simulator().run(circuit, repetitions=shots)
        final_data = result.measurements["final"]
        zeros = int(np.sum(final_data == 0))
        ones = shots - zeros
        return {
            "live_predictions": zeros / shots,
            "dud_predictions": ones / shots,
            "detonations": 0.0
        }
