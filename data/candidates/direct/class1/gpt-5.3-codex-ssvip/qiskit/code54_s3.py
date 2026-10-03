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

    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    probs = {format(i, "03b"): 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        probs[bitstring] = count / shots

    return probs
