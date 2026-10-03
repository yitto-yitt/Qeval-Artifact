# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def or_gate(a, b):
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_result = QuantumRegister(3, 'result')
    cr = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_result, cr)

    # Initialize input registers with classical values
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # Compute bitwise OR using De Morgan's law: a OR b = NOT(NOT a AND NOT b)
    for i in range(3):
        qc.x(qr_result[i])       # result = 1
        qc.x(qr_a[i])            # flip a
        qc.x(qr_b[i])            # flip b
        qc.ccx(qr_a[i], qr_b[i], qr_result[i])  # result ^= (NOT a AND NOT b)
        qc.x(qr_a[i])            # restore a
        qc.x(qr_b[i])            # restore b

    # Measure the result register
    for i in range(3):
        qc.measure(qr_result[i], cr[i])

    # Simulate and collect counts
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
