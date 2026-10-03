# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qa = QuantumRegister(3, 'a')
    qb = QuantumRegister(3, 'b')
    qout = QuantumRegister(3, 'out')
    c = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qa, qb, qout, c)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(qa[i])
        if (b >> i) & 1:
            qc.x(qb[i])

    for i in range(3):
        qc.cx(qa[i], qout[i])
        qc.cx(qb[i], qout[i])
        qc.ccx(qa[i], qb[i], qout[i])

    for i in range(3):
        qc.measure(qout[i], c[i])

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
