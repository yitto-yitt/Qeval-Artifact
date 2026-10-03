# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def visualize_bell_states():
    # Phi+ circuit
    qc_plus = QuantumCircuit(2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure_all()
    
    # Phi- circuit
    qc_minus = QuantumCircuit(2)
    qc_minus.x(0)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.measure_all()
    
    simulator = AerSimulator()
    shots = 1024
    
    # Run Phi+
    t_plus = transpile(qc_plus, simulator)
    result_plus = simulator.run(t_plus, shots=shots).result()
    counts_plus = result_plus.get_counts()
    
    # Run Phi-
    t_minus = transpile(qc_minus, simulator)
    result_minus = simulator.run(t_minus, shots=shots).result()
    counts_minus = result_minus.get_counts()
    
    # Convert to probabilities
    prob_plus = {k: v / shots for k, v in counts_plus.items()}
    prob_minus = {k: v / shots for k, v in counts_minus.items()}
    
    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus
    }
