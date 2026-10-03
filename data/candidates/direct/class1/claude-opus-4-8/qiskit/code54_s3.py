# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a_bits = [(a >> i) & 1 for i in range(3)]
    b_bits = [(b >> i) & 1 for i in range(3)]

    qc = QuantumCircuit(9, 3)
    for i in range(3):
        if a_bits[i]:
            qc.x(i)
        if b_bits[i]:
            qc.x(3 + i)
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)
    for i in range(3):
        qc.measure(6 + i, i)

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
