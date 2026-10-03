# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer.primitives import SamplerV2


def bv_algorithm(s):
    n = len(s)

    qr = QuantumRegister(n + 1, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)

    # Ancilla qubit -> |->  (X followed by H)
    qc.x(n)
    qc.h(range(n + 1))

    # Inner-product oracle: flip the ancilla when x . s == 1
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(i, n)

    # Interference concentrates the amplitude on the hidden string s
    qc.h(range(n))

    # Measure the input register only
    qc.measure(range(n), range(n))

    sampler = SamplerV2()
    job = sampler.run([qc])
    result = job.result()

    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
