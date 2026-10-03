# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def visualize_bell_states():
    # Prepare Phi+ state: (|00> + |11>) / sqrt(2)
    qc_plus = QuantumCircuit(2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure_all()

    # Prepare Phi- state: (|00> - |11>) / sqrt(2)
    qc_minus = QuantumCircuit(2)
    qc_minus.x(0)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.measure_all()

    # Simulate the circuits
    simulator = AerSimulator()
    shots = 1024

    result_plus = simulator.run(qc_plus, shots=shots).result()
    counts_plus = result_plus.get_counts()
    prob_plus = {state: count / shots for state, count in counts_plus.items()}

    result_minus = simulator.run(qc_minus, shots=shots).result()
    counts_minus = result_minus.get_counts()
    prob_minus = {state: count / shots for state, count in counts_minus.items()}

    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus
    }
