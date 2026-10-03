# EVAL_META: task_id=37, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def bv_algorithm(s):
    n = len(s)

    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'meas')
    qc = QuantumCircuit(qr, cr)

    # Initialize ancilla qubit in |-> state
    qc.x(qr[n])
    qc.h(qr[n])

    # Apply Hadamard to all input qubits
    for i in range(n):
        qc.h(qr[i])

    # Apply oracle: CNOT from qubit i to ancilla if corresponding s bit is 1
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(qr[i], qr[n])

    # Apply Hadamard to all input qubits
    for i in range(n):
        qc.h(qr[i])

    # Measure input qubits
    for i in range(n):
        qc.measure(qr[i], cr[i])

    # Run using SamplerV2 with Aer simulator backend
    backend = AerSimulator()
    sampler = SamplerV2(backend)
    job = sampler.run([qc], shots=1024)
    result = job.result()

    # Extract measured bitstrings from the classical register
    counts = result[0].data.meas.get_counts()
    bitstrings = list(counts.keys())

    return [bitstrings, result]
