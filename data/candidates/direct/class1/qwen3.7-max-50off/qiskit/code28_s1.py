# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def visualize_bell_states():
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])
    
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.z(0)
    qc_minus.cx(0, 1)
    qc_minus.measure([0, 1], [0, 1])
    
    sim = AerSimulator()
    shots = 1024
    
    res_plus = sim.run(qc_plus, shots=shots, seed_simulator=42).result()
    counts_plus = res_plus.get_counts()
    
    res_minus = sim.run(qc_minus, shots=shots, seed_simulator=42).result()
    counts_minus = res_minus.get_counts()
    
    prob_plus = {k: v / shots for k, v in counts_plus.items()}
    prob_minus = {k: v / shots for k, v in counts_minus.items()}
    
    return {
        'phi_plus': prob_plus,
        'phi_minus': prob_minus
    }
