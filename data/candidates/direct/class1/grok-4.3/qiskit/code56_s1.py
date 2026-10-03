# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if (a & (1 << i)):
            qc.x(i)
    qc.x(range(n))
    qc.measure(range(n), range(n))
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    prob_dist = {k: v / total for k, v in counts.items()}
    return prob_dist
