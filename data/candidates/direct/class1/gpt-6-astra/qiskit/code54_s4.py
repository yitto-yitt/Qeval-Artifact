# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("a and b must be 3-bit integers (0 through 7).")

    circuit = QuantumCircuit(9, 3)
    for bit in range(3):
        if (a >> bit) & 1:
            circuit.x(bit)
        if (b >> bit) & 1:
            circuit.x(bit + 3)
        circuit.ccx(bit, bit + 3, bit + 6)

    circuit.measure([6, 7, 8], [0, 1, 2])

    counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
