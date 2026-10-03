# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.circuit.library import XGate, HGate, CXGate

def visualize_bell_states():
    # Create quantum and classical registers
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    
    # Phi Plus state preparation circuit
    qc_phi_plus = QuantumCircuit(qr, cr)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    qc_phi_plus.measure_all()
    
    # Phi Minus state preparation circuit
    qc_phi_minus = QuantumCircuit(qr, cr)
    qc_phi_minus.h(0)
    qc_phi_minus.x(1)  # Apply X gate to second qubit before entangling
    qc_phi_minus.cx(0, 1)
    qc_phi_minus.measure_all()
    
    # Simulate both circuits
    simulator = AerSimulator()
    
    # Execute phi plus circuit
    job_phi_plus = simulator.run(qc_phi_plus, shots=10000)
    result_phi_plus = job_phi_plus.result()
    counts_phi_plus = result_phi_plus.get_counts(qc_phi_plus)
    
    # Execute phi minus circuit
    job_phi_minus = simulator.run(qc_phi_minus, shots=10000)
    result_phi_minus = job_phi_minus.result()
    counts_phi_minus = result_phi_minus.get_counts(qc_phi_minus)
    
    # Convert counts to probabilities
    total_shots = 10000
    probs_phi_plus = {key: count/total_shots for key, count in counts_phi_plus.items()}
    probs_phi_minus = {key: count/total_shots for key, count in counts_phi_minus.items()}
    
    return {
        'phi_plus': probs_phi_plus,
        'phi_minus': probs_phi_minus
    }
