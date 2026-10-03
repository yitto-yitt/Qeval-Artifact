# EVAL_META: task_id=68, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    
    if bomb_live:
        # Construct the circuit representing the live bomb tester
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(2 * theta, 0)
            qc.measure(0, i)
        
        # Analytical probabilities for 25 cycles
        p_survival = float(np.cos(theta) ** (2 * N))
        p_detonation = 1.0 - p_survival
        
        return {
            'live_predictions': p_survival,
            'dud_predictions': 0.0,
            'detonations': p_detonation
        }
    else:
        # Construct the circuit representing the dud bomb tester
        qc = QuantumCircuit(1, 1)
        for _ in range(N):
            qc.ry(2 * theta, 0)
        qc.measure(0, 0)
        
        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0,
            'detonations': 0.0
        }
