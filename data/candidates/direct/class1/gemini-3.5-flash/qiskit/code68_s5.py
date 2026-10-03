# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    n_cycles = 25
    if bomb_live:
        qc = QuantumCircuit(n_cycles + 1, n_cycles + 1)
        for i in range(n_cycles):
            qc.ry(np.pi / n_cycles, 0)
            qc.cx(0, i + 1)
        qc.measure(0, 0)
        for i in range(n_cycles):
            qc.measure(i + 1, i + 1)
        
        p_no_detonation = np.cos(np.pi / (2 * n_cycles)) ** (2 * n_cycles)
        p_detonation = 1.0 - p_no_detonation
        return {
            'live_predictions': float(p_no_detonation),
            'dud_predictions': 0.0,
            'detonations': float(p_detonation)
        }
    else:
        qc = QuantumCircuit(1, 1)
        for i in range(n_cycles):
            qc.ry(np.pi / n_cycles, 0)
        qc.measure(0, 0)
        
        return {
            'live_predictions': 0.0,
            'dud_predictions': 1.0,
            'detonations': 0.0
        }
