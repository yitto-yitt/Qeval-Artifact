# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def visualize_bell_states():
    simulator = AerSimulator()
    shots = 1024

    # Phi plus: (|00> + |11>)/sqrt(2)
    qc_plus = QuantumCircuit(2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure_all()
    result_plus = simulator.run(qc_plus, shots=shots, seed_simulator=42).result()
    counts_plus = result_plus.get_counts()
    total_plus = sum(counts_plus.values())
    probs_plus = {k: v / total_plus for k, v in counts_plus.items()}

    # Phi minus: (|00> - |11>)/sqrt(2)
    qc_minus = QuantumCircuit(2)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.z(0)
    qc_minus.measure_all()
    result_minus = simulator.run(qc_minus, shots=shots, seed_simulator=42).result()
    counts_minus = result_minus.get_counts()
    total_minus = sum(counts_minus.values())
    probs_minus = {k: v / total_minus for k, v in counts_minus.items()}

    return {'phi_plus': probs_plus, 'phi_minus': probs_minus}
