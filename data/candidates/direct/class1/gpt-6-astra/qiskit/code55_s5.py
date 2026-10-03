# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def or_gate(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a and b must be integers.")
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("a and b must be 3-bit integers (0 through 7).")

    circuit = QuantumCircuit(9, 3)
    for i in range(3):
        if (a >> i) & 1:
            circuit.x(i)
        if (b >> i) & 1:
            circuit.x(i + 3)

        circuit.cx(i, i + 6)
        circuit.cx(i + 3, i + 6)
        circuit.ccx(i, i + 3, i + 6)
        circuit.measure(i + 6, i)

    counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
