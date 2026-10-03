# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    N = 25
    theta = np.pi / N
    shots = 10000

    sim = AerSimulator()

    if bomb_live:
        qc = QuantumCircuit(2, N + 1)

        for i in range(N):
            qc.ry(theta, 0)
            qc.cx(0, 1)
            qc.measure(1, i)
            qc.reset(1)

        qc.measure(0, N)

        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=shots, seed_simulator=42).result()
        counts = result.get_counts()

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            bitstring = bitstring.zfill(N + 1)
            bomb_bits = bitstring[1:]
            photon_bit = bitstring[0]

            if '1' in bomb_bits:
                detonations += count
            elif photon_bit == '0':
                live_predictions += count
            else:
                dud_predictions += count

    else:
        qc = QuantumCircuit(1, 1)

        for i in range(N):
            qc.ry(theta, 0)

        qc.measure(0, 0)

        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=shots, seed_simulator=42).result()
        counts = result.get_counts()

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            if bitstring == '1':
                dud_predictions += count
            else:
                live_predictions += count

    return {
        'live_predictions': live_predictions / shots,
        'dud_predictions': dud_predictions / shots,
        'detonations': detonations / shots
    }
