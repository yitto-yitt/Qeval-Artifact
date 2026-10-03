# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a_int = int(a, 2) if isinstance(a, str) and set(a) <= {"0", "1"} else int(a)
    b_int = int(b, 2) if isinstance(b, str) and set(b) <= {"0", "1"} else int(b)

    a_int &= 0b111
    b_int &= 0b111

    qa = QuantumRegister(3, "a")
    qb = QuantumRegister(3, "b")
    qout = QuantumRegister(3, "out")
    c = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qa, qb, qout, c)

    for i in range(3):
        if (a_int >> i) & 1:
            qc.x(qa[i])
        if (b_int >> i) & 1:
            qc.x(qb[i])

    for i in range(3):
        qc.cx(qa[i], qout[i])
        qc.cx(qb[i], qout[i])
        qc.ccx(qa[i], qb[i], qout[i])
        qc.measure(qout[i], c[i])

    shots = 1024
    backend = AerSimulator(seed_simulator=12345)
    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots=shots).result().get_counts()

    return {k.replace(" ", ""): v / shots for k, v in counts.items()}
