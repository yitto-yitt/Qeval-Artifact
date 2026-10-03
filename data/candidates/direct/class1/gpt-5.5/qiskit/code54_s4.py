# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def and_gate(a, b):
    a = int(a) & 0b111
    b = int(b) & 0b111

    circuit = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            circuit.x(i)
        if (b >> i) & 1:
            circuit.x(3 + i)

    for i in range(3):
        circuit.ccx(i, 3 + i, 6 + i)
        circuit.measure(6 + i, i)

    shots = 1024
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts(circuit)

    return {state: counts.get(state, 0) / shots for state in [format(i, "03b") for i in range(8)]}
