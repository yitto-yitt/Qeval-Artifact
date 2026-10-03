# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    h_op = Operator.from_label("H")
    phased_h_op = Operator(1j * h_op.data)
    return process_fidelity(h_op, phased_h_op)
