# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    if not isinstance(a, int) or not 0 <= a <= 255:
        raise ValueError("a must be an 8-bit integer in the range 0 to 255.")

    circuit = QuantumCircuit(8, 8)
    for qubit in range(8):
        if (a >> qubit) & 1:
            circuit.x(qubit)

    circuit.x(range(8))
    circuit.measure(range(8), range(8))

    counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
