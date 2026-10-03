# EVAL_META: task_id=2, framework=qiskit, class=2
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    return Statevector([1 / 2**0.5, 0, 0, 1 / 2**0.5])
