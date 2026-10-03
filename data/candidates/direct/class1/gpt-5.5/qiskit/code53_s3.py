# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a = int(a) & 0xFF
    b = int(b) & 0xFF

    qc = QuantumCircuit(16, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(8 + i)

    for i in range(8):
        qc.cx(i, 8 + i)

    for i in range(8):
        qc.measure(8 + i, i)

    shots = 1024
    simulator = AerSimulator()
    counts = simulator.run(qc, shots=shots).result().get_counts(qc)

    return {key: value / shots for key, value in counts.items()}
