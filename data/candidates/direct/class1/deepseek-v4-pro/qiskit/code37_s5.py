# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bv_algorithm(s):
    n = len(s)

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(n)
    qc.barrier()

    for q in range(n):
        qc.h(q)
    qc.barrier()

    for i, char in enumerate(s):
        if char == '1':
            qc.cx(i, n)
    qc.barrier()

    for q in range(n):
        qc.h(q)

    for q in range(n):
        qc.measure(q, q)

    sampler = Sampler(mode=AerSimulator())
    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, counts]
