# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def visualize_bell_states():
    def bell_probabilities(phi_minus=False):
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        if phi_minus:
            circuit.z(0)

        probabilities = Statevector.from_instruction(circuit).probabilities_dict()
        return {
            bitstring: round(float(probability), 12)
            for bitstring, probability in sorted(probabilities.items())
            if probability > 1e-12
        }

    return {
        "phi_plus": bell_probabilities(False),
        "phi_minus": bell_probabilities(True),
    }
