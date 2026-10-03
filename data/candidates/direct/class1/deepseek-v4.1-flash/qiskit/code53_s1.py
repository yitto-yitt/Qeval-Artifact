# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    qc = QuantumCircuit(24, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(8 + i)

    for i in range(8):
        qc.cx(i, 16 + i)
        qc.cx(8 + i, 16 + i)

    qc.measure(range(16, 24), range(8))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
