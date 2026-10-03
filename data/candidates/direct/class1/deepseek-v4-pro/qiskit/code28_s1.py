# EVAL_META: task_id=28, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def visualize_bell_states():
    # Build phi_plus circuit: H on qubit 0, CNOT on qubit 0,1
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])

    # Build phi_minus circuit: H on qubit 0, CNOT on qubit 0,1, Z on qubit 0
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.z(0)
    qc_minus.measure([0, 1], [0, 1])

    # Simulate
    simulator = AerSimulator()
    shots = 10000

    # Execute
    result_plus = simulator.run(qc_plus, shots=shots).result()
    result_minus = simulator.run(qc_minus, shots=shots).result()

    counts_plus = result_plus.get_counts()
    counts_minus = result_minus.get_counts()

    # All possible 2-qubit bitstrings
    all_keys = ['00', '01', '10', '11']

    # Convert counts to probabilities
    prob_plus = {key: 0.0 for key in all_keys}
    for bits, cnt in counts_plus.items():
        prob_plus[bits] = cnt / shots

    prob_minus = {key: 0.0 for key in all_keys}
    for bits, cnt in counts_minus.items():
        prob_minus[bits] = cnt / shots

    return {'phi_plus': prob_plus, 'phi_minus': prob_minus}
