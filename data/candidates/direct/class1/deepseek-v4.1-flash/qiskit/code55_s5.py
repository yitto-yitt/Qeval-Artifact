# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(i)
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
