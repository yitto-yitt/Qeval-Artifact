# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    qr_a = QuantumRegister(8, 'a')
    qr_b = QuantumRegister(8, 'b')
    cr = ClassicalRegister(8, 'c')

    qc = QuantumCircuit(qr_a, qr_b, cr)

    # Encode integer a into register a
    for i in range(8):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Encode integer b into register b
    for i in range(8):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # XOR via CNOT: b[i] = a[i] ^ b[i]
    for i in range(8):
        qc.cx(qr_a[i], qr_b[i])

    # Measure the result register
    qc.measure(qr_b, cr)

    # Simulate and collect counts
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Build probability distribution with 8-bit string keys
    total = sum(counts.values())
    probs = {}
    for bitstring, count in counts.items():
        key = bitstring.replace(' ', '').zfill(8)
        probs[key] = count / total

    return probs
