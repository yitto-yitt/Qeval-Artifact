# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    sim = AerSimulator()
    shots = 10000

    # Phi plus: |Φ+⟩ = (|00⟩ + |11⟩) / √2
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])

    # Phi minus: |Φ-⟩ = (|00⟩ - |11⟩) / √2
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.x(0)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.measure([0, 1], [0, 1])

    result_plus = sim.run(qc_plus, shots=shots).result()
    counts_plus = result_plus.get_counts()

    result_minus = sim.run(qc_minus, shots=shots).result()
    counts_minus = result_minus.get_counts()

    def counts_to_probs(counts):
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}

    return {
        'phi_plus': counts_to_probs(counts_plus),
        'phi_minus': counts_to_probs(counts_minus),
    }
