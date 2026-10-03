from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    qr_a = QuantumRegister(8, 'a')
    qr_b = QuantumRegister(8, 'b')
    cr = ClassicalRegister(8, 'c')

    qc = QuantumCircuit(qr_a, qr_b, cr)

    # Initialize register a with bits of integer a
    for i in range(8):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Initialize register b with bits of integer b
    for i in range(8):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # Apply CNOT from each qubit of a to corresponding qubit of b (XOR)
    for i in range(8):
        qc.cx(qr_a[i], qr_b[i])

    # Measure the output register b
    qc.measure(qr_b, cr)

    # Simulate and sample
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
