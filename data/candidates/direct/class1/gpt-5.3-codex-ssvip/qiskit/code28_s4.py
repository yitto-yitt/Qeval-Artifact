# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    shots = 4096
    simulator = AerSimulator()

    def run_counts(circuit):
        compiled = circuit.copy()
        compiled.measure_all()
        result = simulator.run(compiled, shots=shots).result()
        counts = result.get_counts()
        return {k: v / shots for k, v in counts.items()}

    qc_phi_plus = QuantumCircuit(2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)

    qc_phi_minus = QuantumCircuit(2)
    qc_phi_minus.h(0)
    qc_phi_minus.z(0)
    qc_phi_minus.cx(0, 1)

    return {
        "phi_plus": run_counts(qc_phi_plus),
        "phi_minus": run_counts(qc_phi_minus),
    }
