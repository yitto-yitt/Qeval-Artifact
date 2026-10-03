# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def not_gate(a):
    a = int(a) & 0xFF

    circuit = QuantumCircuit(8, 8)

    for i in range(8):
        if (a >> i) & 1:
            circuit.x(i)

    for i in range(8):
        circuit.x(i)

    circuit.measure(range(8), range(8))

    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    shots = 1024
    result = simulator.run(compiled, shots=shots).result()
    counts = result.get_counts(compiled)

    return {k: v / shots for k, v in counts.items()}
