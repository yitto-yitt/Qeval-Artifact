# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / N

    if bomb_live:
        # Live bomb: each cycle applies a small rotation, then measures.
        # The quantum Zeno effect keeps the photon in |0> with high probability.
        # If any measurement yields |1>, the bomb detonates.
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(theta, 0)
            qc.measure(0, i)
            qc.reset(0)

        sim = AerSimulator()
        shots = 100000
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        live_preds = 0
        dets = 0
        for bitstring, count in counts.items():
            if '1' in bitstring:
                dets += count
            else:
                live_preds += count

        return {
            'live_predictions': live_preds / shots,
            'dud_predictions': 0.0,
            'detonations': dets / shots
        }
    else:
        # Dud bomb: no interaction occurs, photon rotates freely.
        # After N rotations of pi/N the total rotation is pi, landing in |1>.
        qc = QuantumCircuit(1, 1)
        for i in range(N):
            qc.ry(theta, 0)
        qc.measure(0, 0)

        sim = AerSimulator()
        shots = 100000
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        dud_preds = counts.get('1', 0)
        live_preds = counts.get('0', 0)

        return {
            'live_predictions': live_preds / shots,
            'dud_predictions': dud_preds / shots,
            'detonations': 0.0
        }
