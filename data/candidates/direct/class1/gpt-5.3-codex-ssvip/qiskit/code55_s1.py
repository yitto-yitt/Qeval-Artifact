# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(3, 3)

    for i in range(3):
        abit = (a >> i) & 1
        bbit = (b >> i) & 1
        if abit | bbit:
            qc.x(i)

    qc.measure(range(3), range(3))

    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    distribution = {format(i, "03b"): 0.0 for i in range(8)}
    for bitstring, count in counts.items():
        distribution[bitstring] = count / shots
    return distribution
