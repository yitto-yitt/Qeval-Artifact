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
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    qc_minus.z(0)
    qc_minus.measure_all()
    
    backend = AerSimulator()
    shots = 10000
    
    # Sample Phi+
    t_plus = transpile(qc_plus, backend)
    counts_plus = backend.run(t_plus, shots=shots).result().get_counts()
    prob_plus = {k: v / shots for k, v in counts_plus.items()}
    
    # Sample Phi-
    t_minus = transpile(qc_minus, backend)
    counts_minus = backend.run(t_minus, shots=shots).result().get_counts()
    prob_minus = {k: v / shots for k, v in counts_minus.items()}
    
    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus
    }
