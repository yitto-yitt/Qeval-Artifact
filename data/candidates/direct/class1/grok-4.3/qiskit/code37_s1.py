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
        if s[i] == "1":
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    backend = AerSimulator()
    sampler = BackendSampler(backend=backend)
    job = sampler.run(qc, shots=1024)
    result = job.result()
    dist = result.quasi_dists[0]
    bitstrings = []
    for key, prob in dist.items():
        if prob > 1e-6:
            bs = format(key, "0" + str(n) + "b")
            bitstrings.append(bs[::-1])
    return [bitstrings, result]
