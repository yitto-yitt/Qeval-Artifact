# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(range(n + 1))

    for i, bit in enumerate(s):
        if bit == "1":
            qc.cx(i, n)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()

    pub_result = result[0]
    counts = pub_result.data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
