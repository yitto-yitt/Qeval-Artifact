# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_controlled_hgate():
    qc = QuantumCircuit(3)
    qc.ch(0, 2)  # Controlled-H with qubit 0 as control and qubit 2 as target
    qc.ch(1, 2)  # Controlled-H with qubit 1 as control and qubit 2 as target
    # To implement a true three-qubit controlled-H (both controls must be 1),
    # we need to use additional gates to ensure both controls are satisfied
    # First, apply a CCX (Toffoli) gate to temporarily store the AND of the two controls
    qc.ccx(0, 1, 2)
    # Then apply H on qubit 2 conditioned on the result
    qc.h(2)
    # Finally, uncompute the CCX by applying it again
    qc.ccx(0, 1, 2)
    return qc
