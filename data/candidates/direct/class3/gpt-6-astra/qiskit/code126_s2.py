# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity


def calculate_phase_difference_fidelity():
    operator = Operator(HGate())
    phase_shifted_operator = Operator(1j * operator.data)
    return process_fidelity(operator, phase_shifted_operator)
