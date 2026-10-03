# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def bv_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n + 1, n)

    # Initialize the output qubit (last qubit) to |1>
    qc.x(n)

    # Apply Hadamard gates to all qubits
    for i in range(n + 1):
        qc.h(i)

    # Apply the oracle: for each bit in s that is '1', apply CNOT
    # from the corresponding input qubit to the output qubit
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)

    # Apply Hadamard gates to the input register
    for i in range(n):
        qc.h(i)

    # Measure the input register
    for i in range(n):
        qc.measure(i, i)

    # Run using Qiskit Sampler with Aer simulator backend
    backend = AerSimulator()
    sampler = Sampler(backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()

    # Extract measured bitstrings from the classical register
    bitstrings = list(result[0].data.c.get_bitstrings())

    return [bitstrings, result]
