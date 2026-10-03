# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_controlled_hgate():
    qc = QuantumCircuit(3)
    qc.ch(0, 2)  # Controlled-H with qubit 0 as control and qubit 2 as target
    qc.ch(1, 2)  # Controlled-H with qubit 1 as control and qubit 2 as target
    # To implement a true three-qubit controlled-H (both controls must be 1),
    # we need to use additional gates to ensure both controls are satisfied
    qc.ccx(0, 1, 2)  # Toffoli gate to set target to 1 only if both controls are 1
    qc.h(2)          # Apply Hadamard on target qubit
    qc.ccx(0, 1, 2)  # Reverse the Toffoli gate
    return qc
