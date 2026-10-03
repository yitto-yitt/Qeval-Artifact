# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    """Zeno Elitzur-Vaidman bomb tester with 25 interaction cycles.

    Per-cycle rotation angle theta = pi/(2N).  A live bomb performs a
    projective measurement of the photon every cycle: if the photon is
    found in |1> the bomb detonates, otherwise the photon collapses back
    to |0>.  A dud bomb performs no measurement so the rotations
    accumulate coherently.  After N cycles with theta = pi/(2N):

      * dud bomb  : total rotation = 2N*theta = pi  ->  photon in |1>
      * live bomb : if no detonation, photon stays in |0>

    The final Z-basis measurement therefore distinguishes "dud" from
    "live" (non-detonating) outcomes, while any intermediate |1>
    measurement outcome corresponds to a real detonation.
    """
    N = 25
    theta = np.pi / (2.0 * N)
    shots = 100_000
    seed = 12345

    sim = AerSimulator()

    if bomb_live:
        # Live bomb -> mid-circuit measurements (absorptions) each cycle.
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(2.0 * theta, 0)
            qc.measure(0, i)
            qc.reset(0)  # collapse photon back to |0> if not absorbed

        counts = sim.run(qc, shots=shots, seed_simulator=seed).result().get_counts()

        det = 0
        live = 0
        for bits, n in counts.items():
            if '1' in bits:
                det += n
            else:
                live += n
        total = det + live
        return {
            'live_predictions': live / total,
            'dud_predictions': 0.0,
            'detonations': det / total,
        }
    else:
        # Dud bomb -> no measurements, rotations accumulate to pi.
        qc = QuantumCircuit(1, 1)
        for _ in range(N):
            qc.ry(2.0 * theta, 0)
        qc.measure(0, 0)

        counts = sim.run(qc, shots=shots, seed_simulator=seed).result().get_counts()

        dud = counts.get('1', 0)
        live = counts.get('0', 0)
        total = dud + live
        return {
            'live_predictions': live / total,
            'dud_predictions': dud / total,
            'detonations': 0.0,
        }
