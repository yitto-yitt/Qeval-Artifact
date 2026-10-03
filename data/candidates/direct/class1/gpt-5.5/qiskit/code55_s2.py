# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a = int(a)
    b = int(b)
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("Inputs a and b must be 3-bit integers in the range 0..7.")

    qa = QuantumRegister(3, "a")
    qb = QuantumRegister(3, "b")
    qout = QuantumRegister(3, "out")
    c = ClassicalRegister(3, "c")
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

    shots = 1024
    simulator = AerSimulator(seed_simulator=12345)
    tqc = transpile(qc, simulator)
    result = simulator.run(tqc, shots=shots).result()
    counts = result.get_counts()

    return {key.replace(" ", ""): value / shots for key, value in counts.items()}
