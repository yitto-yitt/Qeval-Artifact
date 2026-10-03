# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    qc = QuantumCircuit(9, 3)

    # Encode inputs a (q0..q2) and b (q3..q5)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    # Bitwise AND into output qubits q6..q8 using CCX with ancilla |1>
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)

    # Measure output bits only
    qc.measure(6, 0)
    qc.measure(7, 1)
    qc.measure(8, 2)

    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)

    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    # Ensure all 3-bit keys exist
    for i in range(8):
        key = format(i, "03b")
        probs.setdefault(key, 0.0)

    return probs
