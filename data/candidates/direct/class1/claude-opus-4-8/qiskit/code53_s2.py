# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a &= 0xFF
    b &= 0xFF
    qc = QuantumCircuit(16, 8)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(8 + i)
    for i in range(8):
        qc.cx(i, 8 + i)
    for i in range(8):
        qc.measure(8 + i, i)
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
