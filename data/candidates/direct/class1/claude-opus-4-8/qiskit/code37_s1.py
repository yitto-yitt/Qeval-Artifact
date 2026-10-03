# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    backend = AerSimulator()
    tqc = transpile(qc, backend)
    sampler = SamplerV2()
    result = sampler.run([tqc], shots=1024).result()
    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())
    return [bitstrings, result]
