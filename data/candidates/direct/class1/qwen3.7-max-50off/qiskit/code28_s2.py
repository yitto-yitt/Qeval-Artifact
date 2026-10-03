# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    shots = 10000

    # Phi plus: (|00> + |11>) / sqrt(2)
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])

    # Phi minus: (|00> - |11>) / sqrt(2)
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.z(0)
    qc_minus.measure([0, 1], [0, 1])

    simulator = AerSimulator()

    qc_plus_t = transpile(qc_plus, simulator)
    qc_minus_t = transpile(qc_minus, simulator)

    result_plus = simulator.run(qc_plus_t, shots=shots).result()
    result_minus = simulator.run(qc_minus_t, shots=shots).result()

    counts_plus = result_plus.get_counts()
    counts_minus = result_minus.get_counts()

    prob_plus = {k: v / shots for k, v in counts_plus.items()}
    prob_minus = {k: v / shots for k, v in counts_minus.items()}

    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus,
    }
