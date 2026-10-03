# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    qr_a = QuantumRegister(8, 'a')
    qr_b = QuantumRegister(8, 'b')
    qr_out = QuantumRegister(8, 'out')
    cr = ClassicalRegister(8, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_out, cr)

    # Encode input a into qubits
    for i in range(8):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Encode input b into qubits
    for i in range(8):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # XOR via CNOT: out[i] = a[i] ^ b[i]
    for i in range(8):
        qc.cx(qr_a[i], qr_out[i])
        qc.cx(qr_b[i], qr_out[i])

    # Measure output register
    for i in range(8):
        qc.measure(qr_out[i], cr[i])

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
