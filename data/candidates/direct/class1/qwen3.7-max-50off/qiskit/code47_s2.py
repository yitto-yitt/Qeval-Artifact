# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=samples).result()
    counts = result.get_counts(qc)

    heads = counts.get('0', 0)
    tails = counts.get('1', 0)
    total = heads + tails

    return {
        'Heads': heads / total,
        'Tails': tails / total,
    }
