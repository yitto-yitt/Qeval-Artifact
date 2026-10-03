# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)

    # Prepare ancilla qubit in |-> state
    qc.x(n)
    qc.h(n)

    # Apply Hadamard to all input qubits
    for i in range(n):
        qc.h(i)

    # Apply oracle: CNOT from qubit i to ancilla if s[i] == '1'
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)

    # Apply Hadamard to all input qubits
    for i in range(n):
        qc.h(i)

    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    # Run using SamplerV2 with AerSimulator backend
    backend = AerSimulator()
    sampler = SamplerV2(backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()

    # Extract measured bitstrings from the classical register
    counts = result[0].data.c.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
