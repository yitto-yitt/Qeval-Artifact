# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a %= 8
    b %= 8

    qc = QuantumCircuit(9, 3)

    # Prepare the two 3-bit inputs on qubits 0..2 and 3..5
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    # Bitwise AND using Toffoli gates, results on qubits 6..8
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    # Measure output qubits in standard binary order: MSB leftmost
    qc.measure([8, 7, 6], [0, 1, 2])

    backend = AerSimulator()
    counts = backend.run(qc, shots=1024).result().get_counts()

    total_shots = sum(counts.values())
    return {state: count / total_shots for state, count in counts.items()}
