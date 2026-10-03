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
    measurements = cycles + 1 if bomb_live else 1
    for i in range(cycles):
        circuit.append(cirq.ry(e).on(q))
        if bomb_live:
            circuit.append(cirq.measure(q, key=f'm{i}'))
    circuit.append(cirq.measure(q, key=f'm{measurements - 1}'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)

    if bomb_live:
        last_key = f'm{measurements - 1}'
        last = result.measurements[last_key][:, 0]
        intermediate_keys = [f'm{i}' for i in range(cycles)]
        for shot in range(shots):
            if last[shot] == 1:
                detonations += 1
            else:
                triggered = False
                for k in intermediate_keys:
                    if result.measurements[k][shot, 0] == 1:
                        triggered = True
                        break
                if triggered:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        key = 'm0'
        vals = result.measurements[key][:, 0]
        for v in vals:
            if v == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
