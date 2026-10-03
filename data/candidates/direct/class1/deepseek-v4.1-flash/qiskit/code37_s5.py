# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import BackendSamplerV2
from qiskit_aer import AerSimulator

def bv_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'meas')
    qc = QuantumCircuit(qr, cr)
    ancilla = n
    qc.x(ancilla)
    qc.h(ancilla)
    for i in range(n):
        qc.h(i)
    for i, bit in enumerate(s):
        if bit == '1':
            qc.cx(n - 1 - i, ancilla)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), cr)
    backend = AerSimulator()
    sampler = BackendSamplerV2(backend=backend)
    job = sampler.run([qc])
    result = job.result()
    counts = result[0].data.meas.get_counts()
    bitstrings = list(counts.keys())
    return [bitstrings, result]
