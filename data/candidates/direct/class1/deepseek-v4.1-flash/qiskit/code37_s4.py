# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.primitives import BackendSampler
from qiskit_aer import AerSimulator

def bv_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.x(n)
    qc.h(range(n + 1))
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    backend = AerSimulator()
    sampler = BackendSampler(backend=backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()
    bitstrings = result[0].data.c.get_bitstrings()
    return [bitstrings, result]
