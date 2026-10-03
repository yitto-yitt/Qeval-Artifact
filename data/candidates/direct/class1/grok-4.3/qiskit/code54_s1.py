# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a = a & 7
    b = b & 7
    qc = QuantumCircuit(9, 3)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)
    qc.measure([8, 7, 6], [2, 1, 0])
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
