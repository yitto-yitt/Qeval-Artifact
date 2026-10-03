# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    a &= 0xFF
    b &= 0xFF

    qc = QuantumCircuit(8, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)

    for i in range(8):
        if (b >> i) & 1:
            qc.x(i)

    qc.measure(range(8), range(8))

    backend = AerSimulator()
    counts = backend.run(qc, shots=1024).result().get_counts()

    total_shots = sum(counts.values())
    return {bitstring: count / total_shots for bitstring, count in counts.items()}
