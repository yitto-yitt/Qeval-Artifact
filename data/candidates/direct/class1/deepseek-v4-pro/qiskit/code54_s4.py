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
    qc.measure([6, 7, 8], [0, 1, 2])
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
