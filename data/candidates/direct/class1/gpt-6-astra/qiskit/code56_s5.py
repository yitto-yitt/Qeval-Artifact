# EVAL_META: task_id=56, framework=qiskit, class=1
from operator import index

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    a = index(a)
    if not 0 <= a <= 255:
        raise ValueError("a must be an 8-bit integer in the range 0 to 255.")

    circuit = QuantumCircuit(8, 8)
    for bit in range(8):
        if (a >> bit) & 1:
            circuit.x(bit)

    circuit.x(range(8))
    circuit.measure(range(8), range(8))

    counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bits: count / total for bits, count in counts.items()}
