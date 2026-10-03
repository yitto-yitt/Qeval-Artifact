from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)

    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)

    for i in range(3):
        a_q = i
        b_q = 3 + i
        out_q = 6 + i
        qc.cx(a_q, out_q)
        qc.cx(b_q, out_q)
        qc.ccx(a_q, b_q, out_q)

    for i in range(3):
        qc.measure(6 + i, i)

    sim = AerSimulator()
    transpiled = transpile(qc, sim)
    result = sim.run(transpiled, shots=1024).result()
    counts = result.get_counts()

    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}

    return prob_dist
