# EVAL_META: task_id=54, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(i + 3)

    for i in range(3):
        qc.ccx(i, i + 3, i + 6)
        qc.measure(i + 6, i)

    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    shots = 1024
    counts = simulator.run(tqc, shots=shots).result().get_counts()

    return {format(i, "03b"): counts.get(format(i, "03b"), 0) / shots for i in range(8)}
