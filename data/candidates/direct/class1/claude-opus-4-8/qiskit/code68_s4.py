# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = np.pi / (2 * cycles)

    if not bomb_live:
        qc = QuantumCircuit(1, 1)
        for _ in range(cycles):
            qc.rx(theta, 0)
        qc.measure(0, 0)
        sim = AerSimulator()
        counts = sim.run(qc, shots=8192).result().get_counts()
        shots = sum(counts.values())
        dud_predictions = counts.get('1', 0) / shots
        return {
            'live_predictions': 0.0,
            'dud_predictions': dud_predictions,
            'detonations': 0.0,
        }

    qc = QuantumCircuit(2, 2)
    for _ in range(cycles):
        qc.rx(theta, 0)
        qc.cx(0, 1)
        qc.measure(1, 1)
        qc.reset(1)
    qc.measure(0, 0)

    sim = AerSimulator()
    counts = sim.run(qc, shots=8192).result().get_counts()
    shots = sum(counts.values())

    detonations = 0
    live_predictions = 0
    dud_predictions = 0
    for bitstring, n in counts.items():
        bits = bitstring.replace(' ', '')
        photon = bits[-1]
        detector = bits[-2]
        if detector == '1':
            detonations += n
        elif photon == '0':
            live_predictions += n
        else:
            dud_predictions += n

    return {
        'live_predictions': live_predictions / shots,
        'dud_predictions': dud_predictions / shots,
        'detonations': detonations / shots,
    }
