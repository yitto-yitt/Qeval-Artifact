# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def and_gate(a, b):
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("a and b must be 3-bit integers (0 through 7).")

    circuit = QuantumCircuit(9, 3)
    for bit in range(3):
        if (a >> bit) & 1:
            circuit.x(bit)
        if (b >> bit) & 1:
            circuit.x(3 + bit)
        circuit.ccx(bit, 3 + bit, 6 + bit)

    circuit.measure([6, 7, 8], [0, 1, 2])

    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    counts = simulator.run(compiled, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
