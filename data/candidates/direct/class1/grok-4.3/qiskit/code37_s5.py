# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSampler

def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    backend = AerSimulator()
    sampler = BackendSampler(backend=backend)
    job = sampler.run(qc, shots=1024)
    result = job.result()
    quasi = result.quasi_dists[0]
    bitstrings = [format(int(k), '0{}b'.format(n)) for k in quasi.keys()]
    return [bitstrings, result]
