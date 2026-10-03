# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    qr = QuantumRegister(9, "q")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, cr)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr[i])
        if (b >> i) & 1:
            qc.x(qr[3 + i])

    for i in range(3):
        qc.ccx(qr[i], qr[3 + i], qr[6 + i])

    for i in range(3):
        qc.measure(qr[6 + i], cr[i])

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {state: count / total for state, count in counts.items()}
