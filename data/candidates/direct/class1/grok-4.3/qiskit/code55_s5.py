# EVAL_META: task_id=55, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qc = QuantumCircuit(9, 3)
    for i in range(3):
        a_bit = (a >> i) & 1
        b_bit = (b >> i) & 1
        qa = i
        qb = 3 + i
        qo = 6 + i
        if a_bit:
            qc.x(qa)
        if b_bit:
            qc.x(qb)
        qc.x(qa)
        qc.x(qb)
        qc.ccx(qa, qb, qo)
        qc.x(qo)
        qc.x(qa)
        qc.x(qb)
        qc.measure(qo, i)
    sim = AerSimulator()
    qc = transpile(qc, sim)
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    probs = {k: v / 1024.0 for k, v in counts.items()}
    return probs
