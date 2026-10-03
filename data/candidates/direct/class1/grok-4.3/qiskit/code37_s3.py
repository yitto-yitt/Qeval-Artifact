# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    for i in range(n):
        if s[i] == "1":
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    sampler = Sampler()
    job = sampler.run([qc], shots=1024)
    result = job.result()
    quasi_dist = result.quasi_dists[0]
    bitstrings = [bin(int(key))[2:].zfill(n) for key in quasi_dist.keys()]
    return [bitstrings, result]
