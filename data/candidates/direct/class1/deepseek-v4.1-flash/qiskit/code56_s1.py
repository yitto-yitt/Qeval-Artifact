# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)
    for i in range(n):
        qc.x(i)
    qc.measure(range(n), range(n))
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
