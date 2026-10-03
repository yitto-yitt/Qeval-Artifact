# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a_bits = [(a >> i) & 1 for i in range(3)]
    b_bits = [(b >> i) & 1 for i in range(3)]

    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if a_bits[i]:
            qc.x(i)
        if b_bits[i]:
            qc.x(3 + i)

    for i in range(3):
        qc.x(i)
        qc.x(3 + i)
        qc.x(6 + i)
        qc.ccx(i, 3 + i, 6 + i)
        qc.x(i)
        qc.x(3 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    sim = AerSimulator()
    result = sim.run(qc, shots=4096).result()
    counts = result.get_counts()

    total = sum(counts.values())
    dist = {}
    for k, v in counts.items():
        key = k.replace(" ", "").zfill(3)[-3:]
        dist[key] = dist.get(key, 0) + v / total
    return dist
