# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    if not (isinstance(a, int) and isinstance(b, int)):
        raise TypeError("a and b must be integers")
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("a and b must be 3-bit integers in [0, 7]")

    qc = QuantumCircuit(9, 3)

    a_bits = [(a >> i) & 1 for i in range(3)]
    b_bits = [(b >> i) & 1 for i in range(3)]

    for i in range(3):
        if a_bits[i]:
            qc.x(i)
        if b_bits[i]:
            qc.x(3 + i)

    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)

    qc.measure(6, 0)
    qc.measure(7, 1)
    qc.measure(8, 2)

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
