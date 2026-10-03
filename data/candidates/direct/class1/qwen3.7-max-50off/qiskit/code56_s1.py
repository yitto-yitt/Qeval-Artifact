from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    qc = QuantumCircuit(8, 8)

    # Encode the 8-bit integer a into qubits (little-endian: qubit 0 = LSB)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)

    # Apply bitwise NOT (X gate on every qubit)
    for i in range(8):
        qc.x(i)

    # Measure all qubits
    qc.measure(range(8), range(8))

    # Simulate and get counts
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {bitstring: count / total for bitstring, count in counts.items()}

    return probs
