# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(range(n + 1))
    qc.barrier()

    for idx, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(idx, n)

    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))

    sampler = Sampler(backend=AerSimulator())
    job = sampler.run([qc], shots=1)
    result = job.result()

    bitstrings = list(result[0].data.c.get_counts().keys())
    return [bitstrings, result]
