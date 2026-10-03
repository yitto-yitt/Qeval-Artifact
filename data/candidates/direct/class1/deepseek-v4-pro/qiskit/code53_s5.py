# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    a &= 0xFF
    b &= 0xFF
    c = a ^ b

    qc = QuantumCircuit(8, 8)
    for i in range(8):
        if c & (1 << i):
            qc.x(i)

    qc.measure(range(8), range(8))

    counts = AerSimulator().run(qc, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
