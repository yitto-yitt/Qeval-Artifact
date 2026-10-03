# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / N
    shots = 10000

    if bomb_live:
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(theta, 0)
            qc.measure(0, i)

        sim = AerSimulator()
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        live_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            if '1' not in bitstring:
                live_predictions += count
            else:
                detonations += count

        return {
            'live_predictions': live_predictions / shots,
            'dud_predictions': 0.0,
            'detonations': detonations / shots
        }
    else:
        qc = QuantumCircuit(1, 1)
        for i in range(N):
            qc.ry(theta, 0)
        qc.measure(0, 0)

        sim = AerSimulator()
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        dud_predictions = counts.get('1', 0) / shots
        live_predictions = counts.get('0', 0) / shots

        return {
            'live_predictions': live_predictions,
            'dud_predictions': dud_predictions,
            'detonations': 0.0
        }

