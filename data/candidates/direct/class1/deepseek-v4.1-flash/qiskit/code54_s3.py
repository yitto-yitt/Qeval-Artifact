# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    qa = QuantumRegister(3, 'a')
    qb = QuantumRegister(3, 'b')
    qo = QuantumRegister(3, 'o')
    c = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qa, qb, qo, c)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(qa[i])
        if (b >> i) & 1:
            qc.x(qb[i])

    for i in range(3):
        qc.ccx(qa[i], qb[i], qo[i])

    qc.measure(qo, c)

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
