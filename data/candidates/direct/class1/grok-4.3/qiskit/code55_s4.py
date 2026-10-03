# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
def or_gate(a, b):
    or_val = a | b
    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if (or_val >> i) & 1:
            qc.x(i)
    qc.measure(range(3), range(3))
    sim = AerSimulator()
    res = sim.run(qc, shots=1024).result()
    counts = res.get_counts()
    return {k: v / 1024 for k, v in counts.items()}
