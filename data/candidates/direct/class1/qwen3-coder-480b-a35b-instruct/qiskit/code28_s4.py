# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def visualize_bell_states():
    # Create quantum circuits for phi plus and phi minus
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    
    # Phi plus state: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc_phi_plus = QuantumCircuit(qr, cr)
    qc_phi_plus.h(0)  # Apply H gate to first qubit
    qc_phi_plus.cx(0, 1)  # Apply CNOT gate
    qc_phi_plus.measure_all()  # Measure both qubits
    
    # Phi minus state: |Φ-⟩ = (|00⟩ - |11⟩)/√2
    qc_phi_minus = QuantumCircuit(qr, cr)
    qc_phi_minus.h(0)  # Apply H gate to first qubit
    qc_phi_minus.x(0)  # Apply X gate to first qubit before CNOT to create minus sign
    qc_phi_minus.cx(0, 1)  # Apply CNOT gate
    qc_phi_minus.x(0)  # Undo the X gate on first qubit
    qc_phi_minus.measure_all()  # Measure both qubits
    
    # Simulate both circuits
    simulator = AerSimulator()
    
    # Simulate phi plus
    result_phi_plus = simulator.run(qc_phi_plus, shots=1024).result()
    counts_phi_plus = result_phi_plus.get_counts(qc_phi_plus)
    
    # Normalize counts to probabilities
    total_shots = sum(counts_phi_plus.values())
    prob_dist_phi_plus = {key: count/total_shots for key, count in counts_phi_plus.items()}
    
    # Simulate phi minus
    result_phi_minus = simulator.run(qc_phi_minus, shots=1024).result()
    counts_phi_minus = result_phi_minus.get_counts(qc_phi_minus)
    
    # Normalize counts to probabilities
    total_shots = sum(counts_phi_minus.values())
    prob_dist_phi_minus = {key: count/total_shots for key, count in counts_phi_minus.items()}
    
    return {
        'phi_plus': prob_dist_phi_plus,
        'phi_minus': prob_dist_phi_minus
    }
