# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / N
    if bomb_live:
        survive = (np.cos(theta / 2) ** 2) ** N
        return {'live_predictions': float(survive), 'dud_predictions': 0.0, 'detonations': float(1.0 - survive)}
    else:
        qc = QuantumCircuit(1)
        for _ in range(N):
            qc.ry(theta, 0)
        sv = Statevector(qc)
        probs = sv.probabilities_dict()
        dud_p = probs.get('1', 0.0)
        return {'live_predictions': 0.0, 'dud_predictions': float(dud_p), 'detonations': 0.0}
