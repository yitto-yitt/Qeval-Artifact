# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qa = QuantumRegister(3, "a")
    qb = QuantumRegister(3, "b")
    qo = QuantumRegister(3, "out")
    c = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qa, qb, qo, c)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(qa[i])
        if (b >> i) & 1:
            qc.x(qb[i])

    for i in range(3):
        qc.cx(qa[i], qo[i])
        qc.cx(qb[i], qo[i])
        qc.ccx(qa[i], qb[i], qo[i])

    qc.measure(qo, c)

    shots = 1024
    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    counts = simulator.run(tqc, shots=shots).result().get_counts()

    return {format(i, "03b"): counts.get(format(i, "03b"), 0) / shots for i in range(8) if counts.get(format(i, "03b"), 0) > 0}
