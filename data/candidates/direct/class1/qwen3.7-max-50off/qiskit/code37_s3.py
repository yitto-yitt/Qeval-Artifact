# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def bv_algorithm(s):
    n = len(s)

    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)

    # Initialize ancilla qubit to |-> state
    qc.x(n)
    qc.h(n)

    # Apply Hadamard to all input qubits to create superposition
    for i in range(n):
        qc.h(i)

    # Oracle: apply CNOT from qubit i to ancilla where s[i] == '1'
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)

    # Apply Hadamard to all input qubits for interference
    for i in range(n):
        qc.h(i)

    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    # Run using SamplerV2 with Aer simulator backend
    backend = AerSimulator()
    sampler = SamplerV2(mode=backend)

    job = sampler.run([qc], shots=1024)
    result = job.result()

    # Extract measured bitstrings from the classical register
    pub_result = result[0]
    counts = pub_result.data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
