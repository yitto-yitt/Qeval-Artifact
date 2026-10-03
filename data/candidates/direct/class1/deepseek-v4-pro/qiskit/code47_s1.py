# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    backend = AerSimulator()
    job = backend.run(qc, shots=samples)
    result = job.result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    prob_0 = counts.get('0', 0) / total
    prob_1 = counts.get('1', 0) / total
    return {'Heads': prob_0, 'Tails': prob_1}
