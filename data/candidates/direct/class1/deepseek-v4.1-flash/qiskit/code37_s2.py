# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSampler
from qiskit_aer import AerSimulator


def bv_algorithm(s):
    n = len(s)

    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n))
    qc.h(n)

    for i, bit in enumerate(s):
        if bit == "1":
            qc.cx(i, n)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    backend = AerSimulator()
    sampler = BackendSampler(backend=backend)
    result = sampler.run([qc]).result()

    bitstrings = result[0].data.meas.get_bitstrings()

    return [bitstrings, result]
