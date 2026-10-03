# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
def visualize_bell_states():
    qc_plus = QuantumCircuit(2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_minus = QuantumCircuit(2)
    qc_minus.h(0)
    qc_minus.z(0)
    qc_minus.cx(0, 1)
    probs_plus = Statevector(qc_plus).probabilities_dict()
    probs_minus = Statevector(qc_minus).probabilities_dict()
    return {'phi_plus': probs_plus, 'phi_minus': probs_minus}
