# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    n = 8
    qr_a = QuantumRegister(n, 'a')
    qr_b = QuantumRegister(n, 'b')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr_a, qr_b, cr)
    for i in range(n):
        if (a >> i) & 1:
            qc.x(qr_a[i])
    for i in range(n):
        if (b >> i) & 1:
            qc.x(qr_b[i])
    for i in range(n):
        qc.cx(qr_b[i], qr_a[i])
    qc.measure(qr_a, cr)
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
