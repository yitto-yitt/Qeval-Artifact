# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def visualize_bell_states():
    simulator = AerSimulator()
    shots = 1024
    # Phi+
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])
    counts_plus = simulator.run(qc_plus, shots=shots).result().get_counts()
    probs_plus = {k: v / shots for k, v in counts_plus.items()}
    # Phi-
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.z(0)
    qc_minus.cx(0, 1)
    qc_minus.measure([0, 1], [0, 1])
    counts_minus = simulator.run(qc_minus, shots=shots).result().get_counts()
    probs_minus = {k: v / shots for k, v in counts_minus.items()}
    return {"phi_plus": probs_plus, "phi_minus": probs_minus}
