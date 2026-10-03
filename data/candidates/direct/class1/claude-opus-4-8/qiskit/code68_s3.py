# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = np.pi / (2 * cycles)

    qc = QuantumCircuit(2, 2)
    for _ in range(cycles):
        qc.ry(theta, 0)
        if bomb_live:
            qc.cx(0, 1)
    qc.measure(0, 0)
    qc.measure(1, 1)

    sim = AerSimulator()
    shots = 8192
    counts = sim.run(qc, shots=shots).result().get_counts()

    live_predictions = 0.0
    dud_predictions = 0.0
    detonations = 0.0

    for bitstring, count in counts.items():
        prob = count / shots
        q1 = bitstring[-2]
        q0 = bitstring[-1]
        if bomb_live:
            if q1 == '1':
                detonations += prob
            else:
                if q0 == '0':
                    live_predictions += prob
                else:
                    dud_predictions += prob
        else:
            if q0 == '1':
                dud_predictions += prob
            else:
                dud_predictions += prob

    return {
        'live_predictions': live_predictions,
        'dud_predictions': dud_predictions,
        'detonations': detonations,
    }
