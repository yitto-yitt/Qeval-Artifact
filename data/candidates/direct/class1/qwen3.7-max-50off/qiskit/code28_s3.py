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
    
    sv_plus = Statevector.from_instruction(qc_plus)
    sv_minus = Statevector.from_instruction(qc_minus)
    
    return {
        'phi_plus': sv_plus.probabilities_dict(),
        'phi_minus': sv_minus.probabilities_dict()
    }
