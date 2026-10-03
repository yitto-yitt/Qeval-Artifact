# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def and_gate(a, b):
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_out = QuantumRegister(3, 'out')
    cr = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_out, cr)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    for i in range(3):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    for i in range(3):
        qc.ccx(qr_a[i], qr_b[i], qr_out[i])

    qc.measure(qr_out, cr)

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
