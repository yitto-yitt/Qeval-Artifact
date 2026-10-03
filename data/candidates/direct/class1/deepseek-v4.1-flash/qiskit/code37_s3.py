# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n, "q")
    ar = QuantumRegister(1, "a")
    cr = ClassicalRegister(n, "c")

    qc = QuantumCircuit(qr, ar, cr)

    qc.x(ar[0])
    qc.h(ar[0])
    qc.h(qr)

    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(qr[i], ar[0])

    qc.h(qr)
    qc.measure(qr, cr)

    sampler = SamplerV2()
    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
