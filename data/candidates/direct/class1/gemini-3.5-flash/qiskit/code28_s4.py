# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def visualize_bell_states():
    # Phi+ state: (|00> + |11>) / sqrt(2)
    qc_plus = QuantumCircuit(2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure_all()
    
    # Phi- state: (|00> - |11>) / sqrt(2)
    qc_minus = QuantumCircuit(2)
    qc_minus.x(0)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.measure_all()
    
    backend = AerSimulator()
    
    # Run Phi+ simulation
    t_plus = transpile(qc_plus, backend)
    counts_plus = backend.run(t_plus, shots=1024).result().get_counts()
    total_plus = sum(counts_plus.values())
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    
    # Run Phi- simulation
    t_minus = transpile(qc_minus, backend)
    counts_minus = backend.run(t_minus, shots=1024).result().get_counts()
    total_minus = sum(counts_minus.values())
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus
    }
