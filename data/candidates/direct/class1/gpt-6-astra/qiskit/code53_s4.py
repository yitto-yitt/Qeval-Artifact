# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    if not (0 <= a <= 255 and 0 <= b <= 255):
        raise ValueError("a and b must be 8-bit unsigned integers.")

    circuit = QuantumCircuit(16, 8)
    for bit in range(8):
        if (a >> bit) & 1:
            circuit.x(bit)
        if (b >> bit) & 1:
            circuit.x(bit + 8)
        circuit.cx(bit, bit + 8)

    circuit.measure(range(8, 16), range(8))
    counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
