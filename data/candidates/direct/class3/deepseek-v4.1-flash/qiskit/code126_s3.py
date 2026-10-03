# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    hadamard = Operator(HGate())
    phased_hadamard = Operator(np.exp(1j * np.pi / 4) * hadamard.data)
    return float(process_fidelity(hadamard, phased_hadamard))
