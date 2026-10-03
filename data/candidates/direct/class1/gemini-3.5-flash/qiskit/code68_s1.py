# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def zeno_elitzur_vaidman_bomb_tester(bomb_live: bool) -> dict:
    N = 25
    shots = 100000
    simulator = AerSimulator()
    
    if bomb_live:
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(np.pi / N, 0)
            qc.measure(0, i)
            if i < N - 1:
                qc.reset(0)
        
        result = simulator.run(qc, shots=shots).result()
        counts = result.get_counts()
        
        all_zeros_key = '0' * N
        survived_counts = counts.get(all_zeros_key, 0)
        
        live_prob = survived_counts / shots
        detonation_prob = 1.0 - live_prob
        dud_prob = 0.0
    else:
        qc = QuantumCircuit(1, 1)
        for _ in range(N):
            qc.ry(np.pi / N, 0)
        qc.measure(0, 0)
        
        result = simulator.run(qc, shots=shots).result()
        counts = result.get_counts()
        
        dud_prob = counts.get('1', 0) / shots
        live_prob = counts.get('0', 0) / shots
        detonation_prob = 0.0
        
    return {
        'live_predictions': live_prob,
        'dud_predictions': dud_prob,
        'detonations': detonation_prob
    }
