# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import Aer


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

    qc.measure([6, 7, 8], [0, 1, 2])

    backend = Aer.get_backend("aer_simulator")
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts(qc)

    probs = {k: v / 1024 for k, v in counts.items()}
    for i in range(8):
        key = format(i, "03b")
        if key not in probs:
            probs[key] = 0.0
    return probs
