# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    sim = AerSimulator()
    result = sim.run(qc, shots=samples).result()
    counts = result.get_counts(qc)
    p0 = counts.get('0', 0) / samples if samples > 0 else 0.0
    p1 = counts.get('1', 0) / samples if samples > 0 else 0.0
    return {'Heads': p0, 'Tails': p1}
