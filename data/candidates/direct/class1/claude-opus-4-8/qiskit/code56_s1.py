# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    qc = QuantumCircuit(8, 8)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
    qc.x(range(8))
    qc.measure(range(8), range(8))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
