# EVAL_META: task_id=37, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit_aer import AerSimulator

def bv_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'c')
    circuit = QuantumCircuit(qr, cr)

    # Ancilla qubit (last) to |-> (X then H)
    circuit.x(qr[n])
    circuit.h(qr[n])

    # Apply Hadamard to all input qubits
    for i in range(n):
        circuit.h(qr[i])

    # Oracle: apply CNOT for each '1' in the secret string
    for i, bit in enumerate(s):
        if bit == '1':
            circuit.cx(qr[i], qr[n])

    # Apply Hadamard again to input qubits
    for i in range(n):
        circuit.h(qr[i])

    # Measure input qubits, reversing the bit order so the output matches s
    for i in range(n):
        circuit.measure(qr[i], cr[n - 1 - i])

    # Run with Qiskit Sampler using AerSimulator
    sampler = Sampler(backend=AerSimulator())
    job = sampler.run([circuit], shots=1024)
    result = job.result()

    # Extract bitstring counts from quasi-probabilities
    quasi_dist = result.quasi_dists[0]
    shots = 1024
    bitstrings = {}
    for int_state, prob in quasi_dist.items():
        bit_str = format(int_state, f'0{n}b')
        bitstrings[bit_str] = round(prob * shots)

    return [bitstrings, result]
