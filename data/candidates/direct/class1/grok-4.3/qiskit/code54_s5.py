# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a_bits = [(a >> i) & 1 for i in range(3)]
    b_bits = [(b >> i) & 1 for i in range(3)]
    qa = QuantumRegister(3, "qa")
    qb = QuantumRegister(3, "qb")
    qout = QuantumRegister(3, "qout")
    c = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qa, qb, qout, c)
    for i in range(3):
        if a_bits[i]:
            qc.x(qa[i])
        if b_bits[i]:
            qc.x(qb[i])
        qc.ccx(qa[i], qb[i], qout[i])
    qc.measure(qout, c)
    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
