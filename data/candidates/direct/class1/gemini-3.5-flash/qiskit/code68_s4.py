# EVAL_META: task_id=68, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    simulator = AerSimulator()
    shots = 100000
    
    if bomb_live:
        # Live bomb: measurement at each cycle
        qc = QuantumCircuit(1, N)
        for i in range(N):
            qc.ry(2 * theta, 0)
            qc.measure(0, i)
        
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts()
        
        detonations = 0
        live_predictions = 0
        dud_predictions = 0
        
        for outcome, count in counts.items():
            # In Qiskit, outcome is a space-separated string if multiple registers,
            # or a single string of bits. Here it's a single string of length N.
            if '1' in outcome:
                detonations += count
            else:
                live_predictions += count
                
        return {
            'live_predictions': live_predictions / shots,
            'dud_predictions': dud_predictions / shots,
            'detonations': detonations / shots
        }
    else:
        # Dud bomb: no intermediate measurements, only final measurement
        qc = QuantumCircuit(1, 1)
        for _ in range(N):
            qc.ry(2 * theta, 0)
        qc.measure(0, 0)
        
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts()
        
        live_predictions = counts.get('0', 0) / shots
        dud_predictions = counts.get('1', 0) / shots
        detonations = 0.0
        
        return {
            'live_predictions': live_predictions,
            'dud_predictions': dud_predictions,
            'detonations': detonations
        }
