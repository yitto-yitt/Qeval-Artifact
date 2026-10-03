# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def bv_algorithm(s: str):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(n)
    qc.h(range(n))
    qc.barrier()
    for i in range(n):
        if s[::-1][i] == '1':
            qc.cx(i, n)
    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))
    
    sampler = Sampler()
    job = sampler.run(qc)
    result = job.result()
    
    quasi_dist = result.quasi_dists[0]
    bitstrings = [format(k, f'0{n}b') for k in quasi_dist.keys()]
    
    return [bitstrings, result]
