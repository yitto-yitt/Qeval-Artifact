# EVAL_META: task_id=49, framework=qiskit, class=3
from qiskit import QuantumCircuit

def simple_elitzur_vaidman():
    """
    Returns a simple 2-qubit Elitzur-Vaidman bomb tester circuit without measurements.
    Qubit 0 represents the photon path, and Qubit 1 represents the bomb.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.h(0)
    return qc
