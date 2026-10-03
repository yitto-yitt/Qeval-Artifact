from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def and_gate(a, b):
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_res = QuantumRegister(3, 'res')
    cr = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_res, cr)

    # Initialize input register a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Initialize input register b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # Apply Toffoli (CCX) gates for bitwise AND
    for i in range(3):
        qc.ccx(qr_a[i], qr_b[i], qr_res[i])

    # Measure result register
    qc.measure(qr_res, cr)

    # Simulate
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
