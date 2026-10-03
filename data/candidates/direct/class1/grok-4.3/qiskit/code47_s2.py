# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    simulator = AerSimulator()
    result = simulator.run(qc, shots=samples).result()
    counts = result.get_counts()
    total = sum(counts.values())
    p0 = counts.get('0', 0) / total
    p1 = counts.get('1', 0) / total
    return {'Heads': p0, 'Tails': p1}
