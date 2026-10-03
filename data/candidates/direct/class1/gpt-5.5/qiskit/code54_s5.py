# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)
        qc.ccx(i, 3 + i, 6 + i)
        qc.measure(6 + i, i)

    shots = 1024
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    return {format(i, "03b"): counts.get(format(i, "03b"), 0) / shots for i in range(8)}
