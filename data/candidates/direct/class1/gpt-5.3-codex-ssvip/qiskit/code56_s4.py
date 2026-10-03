# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    a = int(a) & 0xFF
    bits = format(a, "08b")

    qc = QuantumCircuit(8, 8)

    for i, b in enumerate(reversed(bits)):
        if b == "1":
            qc.x(i)

    for i in range(8):
        qc.x(i)

    qc.measure(range(8), range(8))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())

    return {k: v / total for k, v in counts.items()}
