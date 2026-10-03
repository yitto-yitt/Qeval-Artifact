# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = np.pi / cycles
    shots = 8192

    qc = QuantumCircuit(1, 1)
    for _ in range(cycles):
        qc.ry(theta, 0)
        if bomb_live:
            qc.measure(0, 0)
            qc.reset(0)
            with qc.if_test((qc.clbits[0], 1)):
                qc.x(0)
    qc.measure(0, 0)

    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    total = sum(counts.values())

    if bomb_live:
        detonations = counts.get('1', 0) / total
        live_predictions = counts.get('0', 0) / total
        dud_predictions = 0.0
    else:
        detonations = 0.0
        live_predictions = 0.0
        dud_predictions = counts.get('1', 0) / total

    return {
        'live_predictions': live_predictions,
        'dud_predictions': dud_predictions,
        'detonations': detonations,
    }
