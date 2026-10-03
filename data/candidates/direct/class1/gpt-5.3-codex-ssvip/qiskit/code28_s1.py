# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()

    qc_phi_plus = QuantumCircuit(2, 2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    qc_phi_plus.measure([0, 1], [0, 1])

    qc_phi_minus = QuantumCircuit(2, 2)
    qc_phi_minus.x(0)
    qc_phi_minus.h(0)
    qc_phi_minus.cx(0, 1)
    qc_phi_minus.measure([0, 1], [0, 1])

    shots = 4096
    result_plus = simulator.run(qc_phi_plus, shots=shots).result()
    result_minus = simulator.run(qc_phi_minus, shots=shots).result()

    counts_plus = result_plus.get_counts(qc_phi_plus)
    counts_minus = result_minus.get_counts(qc_phi_minus)

    probs_plus = {k: v / shots for k, v in counts_plus.items()}
    probs_minus = {k: v / shots for k, v in counts_minus.items()}

    return {
        "phi_plus": probs_plus,
        "phi_minus": probs_minus,
    }
