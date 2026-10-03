# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QuantumMachine
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    circuit = QuantumCircuit(1, measurements)
    for i in range(cycles):
        circuit.ry(e, 0)
        if bomb_live:
            circuit.measure(0, i)
    circuit.measure(0, measurements - 1)

    machine = QuantumMachine()
    result = machine.run(circuit, shots=shots)

    if hasattr(result, "get_counts"):
        counts = result.get_counts()
    elif hasattr(result, "counts"):
        counts = result.counts
    else:
        counts = result

    if bomb_live:
        for key, value in counts.items():
            key = str(key)
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
