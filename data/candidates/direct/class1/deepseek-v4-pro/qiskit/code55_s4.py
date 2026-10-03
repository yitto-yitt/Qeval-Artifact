# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a: int, b: int) -> dict:
    output = a | b

    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if (output >> i) & 1:
            qc.x(i)

    qc.measure([0, 1, 2], [0, 1, 2])

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()

    return {key: value / 1024 for key, value in counts.items()}
