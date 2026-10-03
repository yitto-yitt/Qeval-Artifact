# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    n = 8
    qc = QuantumCircuit(2 * n, n)

    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)

    for i in range(n):
        if (b >> i) & 1:
            qc.x(n + i)

    for i in range(n):
        qc.cx(i, n + i)

    for i in range(n):
        qc.measure(n + i, i)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)

    total_shots = sum(counts.values())
    return {state: count / total_shots for state, count in counts.items()}
