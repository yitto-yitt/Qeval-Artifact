# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    shots = int(samples)
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    heads = counts.get('0', 0)
    tails = counts.get('1', 0)
    total = heads + tails
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}

    return {'Heads': heads / total, 'Tails': tails / total}
