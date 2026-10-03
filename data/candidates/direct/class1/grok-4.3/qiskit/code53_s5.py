# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

def xor_gate(a, b):
    qr_a = QuantumRegister(8, "a")
    qr_b = QuantumRegister(8, "b")
    cr = ClassicalRegister(8, "c")
    qc = QuantumCircuit(qr_a, qr_b, cr)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(qr_a[i])
    for i in range(8):
        if (b >> i) & 1:
            qc.x(qr_b[i])
    for i in range(8):
        qc.cx(qr_a[i], qr_b[i])
    qc.measure(qr_b, cr)
    simulator = AerSimulator()
    qc = transpile(qc, simulator)
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
