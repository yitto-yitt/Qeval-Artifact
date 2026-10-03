# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def or_gate(a, b):
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_r = QuantumRegister(3, 'r')
    cr = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_r, cr)

    # Initialize register a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Initialize register b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # Bitwise OR: r_i = a_i XOR b_i XOR (a_i AND b_i) = a_i OR b_i
    for i in range(3):
        qc.cx(qr_a[i], qr_r[i])
        qc.cx(qr_b[i], qr_r[i])
        qc.ccx(qr_a[i], qr_b[i], qr_r[i])

    # Measure result qubits
    qc.measure(qr_r, cr)

    # Simulate
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
