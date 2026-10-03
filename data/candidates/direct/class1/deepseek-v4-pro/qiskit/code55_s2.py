# EVAL_META: task_id=55, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if ((a >> i) & 1) or ((b >> i) & 1):
            qc.x(i)
    qc.measure(range(3), range(3))

    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    counts = job.result().get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
