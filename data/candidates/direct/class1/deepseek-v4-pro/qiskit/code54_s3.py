# EVAL_META: task_id=54, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a &= 0b111
    b &= 0b111

    # 9 qubits: 0-2 for a, 3-5 for b, 6-8 for output
    qc = QuantumCircuit(9, 3)

    # Encode a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)

    # Encode b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)

    # Bitwise AND using Toffoli gates
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    # Measure output register
    for i in range(3):
        qc.measure(6 + i, i)

    backend = AerSimulator()
    counts = backend.run(qc, shots=1024).result().get_counts()
    total_shots = sum(counts.values())

    return {state: count / total_shots for state, count in counts.items()}
