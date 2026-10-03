# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    shots = 4096
    simulator = AerSimulator(seed_simulator=28)

    def run_circuit(phi_minus=False):
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        if phi_minus:
            circuit.z(0)
        circuit.measure([0, 1], [0, 1])

        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts(circuit)

        probabilities = {"00": 0.0, "01": 0.0, "10": 0.0, "11": 0.0}
        for bitstring, count in counts.items():
            probabilities[bitstring] = count / shots

        return probabilities

    return {
        "phi_plus": run_circuit(phi_minus=False),
        "phi_minus": run_circuit(phi_minus=True),
    }
