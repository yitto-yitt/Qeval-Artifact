# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if ((a >> i) & 1) or ((b >> i) & 1):
            qc.x(i)
    qc.measure([0, 1, 2], [0, 1, 2])
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    return {k: v / 1024 for k, v in counts.items()}
