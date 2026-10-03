# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def visualize_bell_states():
    # Bell state |Phi+> = (|00> + |11>)/sqrt(2)
    qc_phi_plus = QuantumCircuit(2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)

    # Bell state |Phi-> = (|00> - |11>)/sqrt(2)
    qc_phi_minus = QuantumCircuit(2)
    qc_phi_minus.h(0)
    qc_phi_minus.z(0)
    qc_phi_minus.cx(0, 1)

    return {
        "phi_plus": Statevector.from_instruction(qc_phi_plus).probabilities_dict(),
        "phi_minus": Statevector.from_instruction(qc_phi_minus).probabilities_dict(),
    }
