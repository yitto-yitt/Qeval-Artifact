# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)

    qr = QuantumRegister(n + 1, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)

    qc.x(qr[n])

    for i in range(n + 1):
        qc.h(qr[i])

    for i, bit in enumerate(s):
        if bit == "1":
            qc.cx(qr[i], qr[n])

    for i in range(n):
        qc.h(qr[i])

    for i in range(n):
        qc.measure(qr[i], cr[n - 1 - i])

    backend = AerSimulator()
    sampler = SamplerV2(backend=backend)

    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = getattr(result[0].data, cr.name).get_counts()
    bitstrings = sorted(counts.keys())

    return [bitstrings, result]
