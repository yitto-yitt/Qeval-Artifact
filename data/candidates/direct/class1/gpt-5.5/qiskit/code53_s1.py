# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a = int(a)
    b = int(b)

    if not (0 <= a <= 255 and 0 <= b <= 255):
        raise ValueError("Inputs a and b must be 8-bit integers in the range 0..255.")

    circuit = QuantumCircuit(24, 8)

    for i in range(8):
        if (a >> i) & 1:
            circuit.x(i)
        if (b >> i) & 1:
            circuit.x(8 + i)

    for i in range(8):
        circuit.cx(i, 16 + i)
        circuit.cx(8 + i, 16 + i)
        circuit.measure(16 + i, i)

    shots = 1024
    simulator = AerSimulator(seed_simulator=12345)
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    return {key.replace(" ", ""): value / shots for key, value in counts.items()}
