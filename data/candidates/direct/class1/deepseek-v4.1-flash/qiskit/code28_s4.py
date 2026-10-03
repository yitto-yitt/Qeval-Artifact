# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def visualize_bell_states():
    def _probabilities(phi_minus=False):
        qc = QuantumCircuit(2)
        qc.h(0)
        if phi_minus:
            qc.z(0)
        qc.cx(0, 1)
        sv = Statevector(qc)
        probs = sv.probabilities_dict()
        return {
            bitstring: round(float(p), 12)
            for bitstring, p in probs.items()
            if p > 1e-12
        }

    return {
        'phi_plus': _probabilities(phi_minus=False),
        'phi_minus': _probabilities(phi_minus=True),
    }
