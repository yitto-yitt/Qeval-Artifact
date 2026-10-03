# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def visualize_bell_states():
    def _probabilities(phase):
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        if phase == -1:
            qc.z(0)
        return {
            bitstring: float(probability)
            for bitstring, probability in Statevector.from_instruction(qc).probabilities_dict().items()
        }

    return {
        "phi_plus": _probabilities(1),
        "phi_minus": _probabilities(-1),
    }
