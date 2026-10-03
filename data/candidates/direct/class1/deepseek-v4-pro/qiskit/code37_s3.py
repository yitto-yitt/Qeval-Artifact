# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'meas')
    qc = QuantumCircuit(qr, cr)

    qc.x(qr[n])
    qc.h(qr)

    qc.barrier()
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(qr[i], qr[n])

    qc.barrier()
    qc.h(qr[:n])
    qc.measure(qr[:n], cr)

    sampler = SamplerV2()
    job = sampler.run([qc])
    result = job.result()

    counts = result[0].data.meas.get_counts()
    bitstrings = []
    for bits, count in counts.items():
        bitstrings.extend([bits] * count)

    return [bitstrings, result]
