# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(n)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()
    bitstrings = result[0].data.c.get_bitstrings()
    return [bitstrings, result]
