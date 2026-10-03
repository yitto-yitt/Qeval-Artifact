# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit import execute


def visualize_bell_states():
    # Create quantum circuits for phi+ and phi- states
    # Phi+ = (|00> + |11>) / sqrt(2)
    qc_phi_plus = QuantumCircuit(2, 2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    
    # Phi- = (|00> - |11>) / sqrt(2)
    qc_phi_minus = QuantumCircuit(2, 2)
    qc_phi_minus.x(0)  # Start with |10>
    qc_phi_minus.h(0)
    qc_phi_minus.cx(0, 1)
    
    # Simulate both circuits
    simulator = AerSimulator()
    
    # Execute phi+ circuit
    job_plus = execute(qc_phi_plus, simulator, shots=1000)
    result_plus = job_plus.result()
    counts_plus = result_plus.get_counts(qc_phi_plus)
    
    # Execute phi- circuit
    job_minus = execute(qc_phi_minus, simulator, shots=1000)
    result_minus = job_minus.result()
    counts_minus = result_minus.get_counts(qc_phi_minus)
    
    # Convert to probability distributions
    total_shots = 1000
    prob_dist_plus = {key: count/total_shots for key, count in counts_plus.items()}
    prob_dist_minus = {key: count/total_shots for key, count in counts_minus.items()}
    
    return {
        'phi_plus': prob_dist_plus,
        'phi_minus': prob_dist_minus
    }
