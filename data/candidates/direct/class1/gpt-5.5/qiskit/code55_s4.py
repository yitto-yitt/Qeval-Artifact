# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    shots = 1024
    counts = simulator.run(tqc, shots=shots).result().get_counts()

    return {k: v / shots for k, v in counts.items()}
