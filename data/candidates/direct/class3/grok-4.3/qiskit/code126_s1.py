# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    op1 = Operator(HGate())
    op2 = Operator(1j * HGate().to_matrix())
    return process_fidelity(op1, op2)
