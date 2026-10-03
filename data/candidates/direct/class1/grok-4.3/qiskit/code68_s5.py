# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    shots = 10000
    sim = AerSimulator()
    if not bomb_live:
        qc = QuantumCircuit(1, 1)
        for _ in range(N):
            qc.ry(theta, 0)
        qc.measure(0, 0)
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()
        dud_prob = counts.get('1', 0) / shots
        live_prob = counts.get('0', 0) / shots
        det_prob = 0.0
        return {'live_predictions': live_prob, 'dud_predictions': dud_prob, 'detonations': det_prob}
    else:
        num_clbits = N + 1
        qc = QuantumCircuit(1, num_clbits)
        for i in range(N):
            qc.ry(theta, 0)
            qc.measure(0, i)
        qc.measure(0, N)
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()
        det = 0
        live = 0
        dud = 0
        for bitstr, cnt in counts.items():
            checks = bitstr[1:]
            if '1' in checks:
                det += cnt
            else:
                final = bitstr[0]
                if final == '0':
                    live += cnt
                else:
                    dud += cnt
        live_prob = live / shots
        dud_prob = dud / shots
        det_prob = det / shots
        return {'live_predictions': live_prob, 'dud_predictions': dud_prob, 'detonations': det_prob}
