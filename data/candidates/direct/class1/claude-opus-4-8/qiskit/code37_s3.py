# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(n)
    for i in range(n):
        qc.h(i)
    qc.barrier()
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n)
    qc.barrier()
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.measure(i, i)

    backend = AerSimulator()
    sampler = SamplerV2.from_backend(backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()
    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())
    return [bitstrings, result]
