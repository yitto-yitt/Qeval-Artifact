# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / (2 * N)
    num_shots = 1024
    live_pred = 0.0
    dud_pred = 0.0
    deton = 0.0
    if not bomb_live:
        qc = QuantumCircuit(1, 1)
        qc.ry(np.pi / 2, 0)
        qc.measure(0, 0)
        sim = AerSimulator()
        qc = transpile(qc, sim)
        result = sim.run(qc, shots=num_shots).result()
        counts = result.get_counts()
        dud_pred = counts.get('1', 0) / num_shots
        live_pred = counts.get('0', 0) / num_shots
    else:
        for _ in range(num_shots):
            exploded = False
            for _ in range(N):
                p_explode = np.sin(theta) ** 2
                if np.random.rand() < p_explode:
                    exploded = True
                    break
            if exploded:
                deton += 1
            else:
                live_pred += 1
        live_pred /= num_shots
        deton /= num_shots
    return {
        'live_predictions': live_pred,
        'dud_predictions': dud_pred,
        'detonations': deton
    }
