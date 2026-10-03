# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, RY
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << qvm.Measure(qubits[0], cbits[i])
    prog << qvm.Measure(qubits[0], cbits[measurements - 1])

    raw_counts = qvm.run_with_configuration(prog, cbits, shots)

    # Normalize keys to fixed-width bit strings with cbit index 0 on the right,
    # matching Qiskit's classical bit ordering (rightmost = c[0]).
    counts = {}
    for key, value in raw_counts.items():
        key = key.zfill(measurements)
        counts[key] = counts.get(key, 0) + value

    if bomb_live:
        # In Qiskit key string, index 0 is the last measured cbit (measurements-1),
        # and the rest correspond to the per-cycle measurements.
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
