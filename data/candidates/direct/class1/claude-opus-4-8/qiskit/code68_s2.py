# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = np.pi / (2 * cycles)

    if not bomb_live:
        qc = QuantumCircuit(1, 1)
        for _ in range(cycles):
            qc.rx(theta, 0)
        qc.measure(0, 0)

        sim = AerSimulator()
        counts = sim.run(qc, shots=8192).result().get_counts()
        shots = sum(counts.values())
        p_one = counts.get('1', 0) / shots

        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0 - p_one,
            'detonations': 0.0,
        }

    qc = QuantumCircuit(2, 1)
    for _ in range(cycles):
        qc.rx(theta, 0)
        qc.cx(0, 1)
        qc.measure(0, 0)
        qc.reset(0)
        with qc.if_test((0, 1)):
            pass

    qc.measure(1, 0)

    sim = AerSimulator()
    counts = sim.run(qc, shots=8192).result().get_counts()
    shots = sum(counts.values())

    p_detonation = counts.get('1', 0) / shots
    p_live_prediction = counts.get('0', 0) / shots

    return {
        'live_predictions': p_live_prediction,
        'dud_predictions': 0.0,
        'detonations': p_detonation,
    }
