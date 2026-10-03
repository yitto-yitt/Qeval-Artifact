# EVAL_META: task_id=55, framework=qiskit, class=1
from operator import index

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a, b = index(a), index(b)
    if not (0 <= a < 8 and 0 <= b < 8):
        raise ValueError("a and b must be 3-bit integers in the range 0 to 7.")

    circuit = QuantumCircuit(9, 3)
    for bit in range(3):
        if (a >> bit) & 1:
            circuit.x(bit)
        if (b >> bit) & 1:
            circuit.x(bit + 3)

        circuit.cx(bit, bit + 6)
        circuit.cx(bit + 3, bit + 6)
        circuit.ccx(bit, bit + 3, bit + 6)
        circuit.measure(bit + 6, bit)

    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    counts = simulator.run(compiled, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
