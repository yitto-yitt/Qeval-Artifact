# EVAL_META: task_id=53, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    qc = QuantumCircuit(16, 8)
    for i in range(8):
        if (a & (1 << i)):
            qc.x(i)
        if (b & (1 << i)):
            qc.x(8 + i)
    for i in range(8):
        qc.cx(i, 8 + i)
    qc.measure([8 + i for i in range(8)], list(range(8)))
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
