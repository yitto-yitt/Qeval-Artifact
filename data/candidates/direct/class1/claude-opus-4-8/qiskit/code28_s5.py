# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()
    shots = 4096

    def sample(circuit):
        circuit.measure_all()
        result = simulator.run(circuit, shots=shots).result()
        counts = result.get_counts()
        return {bitstring: count / shots for bitstring, count in counts.items()}

    phi_plus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)

    phi_minus = QuantumCircuit(2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)

    return {
        'phi_plus': sample(phi_plus),
        'phi_minus': sample(phi_minus),
    }
