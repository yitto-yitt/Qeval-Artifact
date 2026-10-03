# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def and_gate(a, b):
    qc = QuantumCircuit(9, 3)
    for i in range(3):
        if (a & (1 << i)):
            qc.x(i)
        if (b & (1 << i)):
            qc.x(3 + i)
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)
    qc.measure([6, 7, 8], [0, 1, 2])
    sim = AerSimulator()
    res = sim.run(qc, shots=1024).result()
    counts = res.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
