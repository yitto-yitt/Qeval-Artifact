# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, RY, measure
from numpy import pi


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qubits = list(range(1))
    cbits = list(range(measurements))

    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << measure(qubits[0], cbits[i])
    prog << measure(qubits[0], cbits[measurements - 1])

    qvm.run(prog, shots)
    raw_counts = qvm.result().get_counts()

    # Normalize key bit-order to match Qiskit's (cbit index 0 first)
    counts = {}
    for key, value in raw_counts.items():
        norm = key[::-1]
        counts[norm] = counts.get(norm, 0) + value

    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1'] if '1' in counts else 0
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
