# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qa = QuantumRegister(3, 'a')
    qb = QuantumRegister(3, 'b')
    qo = QuantumRegister(3, 'o')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qa, qb, qo, cr)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qa[i])
        if (b >> i) & 1:
            qc.x(qb[i])
        qc.x(qo[i])
        qc.x(qa[i])
        qc.x(qb[i])
        qc.ccx(qa[i], qb[i], qo[i])
        qc.x(qa[i])
        qc.x(qb[i])
    qc.measure(qo, cr)
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
