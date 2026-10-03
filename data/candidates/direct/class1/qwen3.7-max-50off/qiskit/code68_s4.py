# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    shots = 100000

    simulator = AerSimulator()

    if bomb_live:
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(theta, 0)
            qc.measure(0, i)

        result = simulator.run(qc, shots=shots, seed_simulator=42).result()
        counts = result.get_counts()

        live_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            if '1' in bitstring:
                detonations += count
            else:
                live_predictions += count

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

        result = simulator.run(qc, shots=shots, seed_simulator=42).result()
        counts = result.get_counts()

        dud_predictions = counts.get('1', 0) / shots
        live_predictions = counts.get('0', 0) / shots

        return {
            'live_predictions': live_predictions,
            'dud_predictions': dud_predictions,
            'detonations': 0.0
        }
