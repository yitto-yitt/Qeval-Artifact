# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def and_gate(a, b):
    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    backend = AerSimulator()
    counts = backend.run(qc, shots=1024).result().get_counts(qc)
    total = sum(counts.values())

    return {k: v / total for k, v in counts.items()}
